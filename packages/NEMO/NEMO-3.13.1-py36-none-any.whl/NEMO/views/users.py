from datetime import timedelta
from http import HTTPStatus
from logging import getLogger
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from NEMO.decorators import staff_member_required
from NEMO.forms import UserForm, UserPreferencesForm
from NEMO.models import (
	ActivityHistory,
	Area,
	AreaAccessRecord,
	PhysicalAccessLevel,
	Project,
	Reservation,
	StaffCharge,
	Tool,
	UsageEvent,
	User,
	record_active_state,
	record_local_many_to_many_changes,
)
from NEMO.views.customization import get_customization
from NEMO.views.pagination import SortedPaginator

users_logger = getLogger(__name__)

@staff_member_required
@require_GET
def users(request):
	all_users = User.objects.all()

	page = SortedPaginator(all_users, request, order_by="last_name").get_current_page()

	return render(request, "users/users.html", {"page": page, "users": all_users})


@staff_member_required
@require_http_methods(['GET', 'POST'])
def create_or_modify_user(request, user_id):
	identity_service = get_identity_service()
	# Get access levels and sort by area category
	access_levels = list(PhysicalAccessLevel.objects.all().only('name', 'area'))
	access_level_for_sort = list(set([ancestor for access in access_levels for ancestor in access.area.get_ancestors(include_self=True)]))
	access_level_for_sort.sort(key=lambda x:x.tree_category())
	area_access_levels = Area.objects.filter(id__in=[area.id for area in access_level_for_sort])
	dict_area = {}
	for access in access_levels:
		dict_area.setdefault(access.area.id,[]).append(access)

	dictionary = {
		'projects': Project.objects.filter(active=True, account__active=True),
		'tools': Tool.objects.filter(visible=True),
		'area_access_dict': dict_area,
		'area_access_levels': area_access_levels,
		'one_year_from_now': timezone.now() + timedelta(days=365),
		'identity_service_available': identity_service.get('available', False),
		'identity_service_domains': identity_service.get('domains', []),
	}
	try:
		user = User.objects.get(id=user_id)
	except:
		user = None

	timeout = identity_service.get('timeout', 3)
	site_title = get_customization('site_title')
	if dictionary['identity_service_available']:
		try:
			result = requests.get(urljoin(identity_service['url'], '/areas/'), timeout=timeout)
			if result.status_code == HTTPStatus.OK:
				dictionary['externally_managed_physical_access_levels'] = result.json()
			else:
				dictionary['identity_service_available'] = False
				warning_message = f"The identity service encountered a problem while attempting to return a list of externally managed areas. The administrator has been notified to resolve the problem."
				dictionary['warning'] = warning_message
				warning_message += ' The HTTP error was {}: {}'.format(result.status_code, result.text)
				users_logger.error(warning_message)
		except Exception as e:
			dictionary['identity_service_available'] = False
			warning_message = f"There was a problem communicating with the identity service. {site_title} is unable to retrieve the list of externally managed areas. The administrator has been notified to resolve the problem."
			dictionary['warning'] = warning_message
			warning_message += ' An exception was encountered: ' + type(e).__name__ + ' - ' + str(e)
			users_logger.error(warning_message)
	elif identity_service:
		# display warning if identity service is defined but disabled
		dictionary['warning'] = 'The identity service is disabled. You will not be able to modify externally managed physical access levels, reset account passwords, or unlock accounts.'

	if request.method == 'GET':
		dictionary['form'] = UserForm(instance=user)
		try:
			if dictionary['identity_service_available'] and user and user.is_active and user.domain:
				parameters = {
					'username': user.username,
					'domain': user.domain,
				}
				result = requests.get(identity_service['url'], parameters, timeout=timeout)
				if result.status_code == HTTPStatus.OK:
					dictionary['user_identity_information'] = result.json()
				elif result.status_code == HTTPStatus.NOT_FOUND:
					dictionary['warning'] = "The identity service could not find username {} on the {} domain. Does the user's account reside on a different domain? If so, select that domain now and save the user information.".format(user.username, user.domain)
				else:
					dictionary['identity_service_available'] = False
					warning_message = 'The identity service encountered a problem while attempting to search for a user. The administrator has been notified to resolve the problem.'
					dictionary['warning'] = warning_message
					warning_message += ' The HTTP error was {}: {}'.format(result.status_code, result.text)
					users_logger.error(warning_message)
		except Exception as e:
			dictionary['identity_service_available'] = False
			warning_message = f"There was a problem communicating with the identity service. {site_title} is unable to search for a user. The administrator has been notified to resolve the problem."
			dictionary['warning'] = warning_message
			warning_message += ' An exception was encountered: ' + type(e).__name__ + ' - ' + str(e)
			users_logger.error(warning_message)
		return render(request, 'users/create_or_modify_user.html', dictionary)
	elif request.method == 'POST':
		form = UserForm(request.POST, instance=user)
		dictionary['form'] = form
		if not form.is_valid():
			return render(request, 'users/create_or_modify_user.html', dictionary)

		# Remove the user account from the domain if it's deactivated, changed domain, or changed username...
		if dictionary['identity_service_available'] and user:
			no_longer_active = form.initial['is_active'] is True and form.cleaned_data['is_active'] is False
			domain_switched = form.initial['domain'] != '' and form.initial['domain'] != form.cleaned_data['domain']
			username_changed = form.initial['username'] != form.cleaned_data['username']
			if no_longer_active or domain_switched or username_changed:
				parameters = {
					'username': form.initial['username'],
					'domain': form.initial['domain'],
				}
				try:
					result = requests.delete(identity_service['url'], data=parameters, timeout=timeout)
					# If the delete succeeds, or the user is not found, then everything is ok.
					if result.status_code not in (HTTPStatus.OK, HTTPStatus.NOT_FOUND):
						dictionary['identity_service_available'] = False
						users_logger.error('The identity service encountered a problem while attempting to delete a user. The HTTP error is {}: {}'.format(result.status_code, result.text))
						dictionary['warning'] = 'The user information was not modified because the identity service could not delete the corresponding domain account. The administrator has been notified to resolve the problem.'
						return render(request, 'users/create_or_modify_user.html', dictionary)
				except Exception as e:
					dictionary['identity_service_available'] = False
					users_logger.error('There was a problem communicating with the identity service while attempting to delete a user. An exception was encountered: ' + type(e).__name__ + ' - ' + str(e))
					dictionary['warning'] = 'The user information was not modified because the identity service could not delete the corresponding domain account. The administrator has been notified to resolve the problem.'
					return render(request, 'users/create_or_modify_user.html', dictionary)

		# Ensure the user account is added and configured correctly on the current domain if the user is active...
		if dictionary['identity_service_available'] and form.cleaned_data['is_active']:
			parameters = {
				'username': form.cleaned_data['username'],
				'domain': form.cleaned_data['domain'],
				'badge_number': form.cleaned_data.get('badge_number', ''),
				'email': form.cleaned_data.get('email'),
				'access_expiration': form.cleaned_data.get('access_expiration'),
				'requested_areas': request.POST.getlist('externally_managed_access_levels'),
			}
			try:
				if len(parameters['requested_areas']) > 0 and not parameters['badge_number']:
					dictionary['warning'] = 'A user must have a badge number in order to have area access. Please enter the badge number first, then grant access to areas.'
					return render(request, 'users/create_or_modify_user.html', dictionary)
				result = requests.put(identity_service['url'], data=parameters, timeout=timeout)
				if result.status_code == HTTPStatus.NOT_FOUND:
					dictionary['warning'] = 'The username was not found on this domain. Did you spell the username correctly in this form and did you select the correct domain? Ensure the user exists on the domain in order to proceed.'
					return render(request, 'users/create_or_modify_user.html', dictionary)
				if result.status_code != HTTPStatus.OK:
					dictionary['identity_service_available'] = False
					users_logger.error('The identity service encountered a problem while attempting to modify a user. The HTTP error is {}: {}'.format(result.status_code, result.text))
					dictionary['warning'] = 'The user information was not modified because the identity service encountered a problem while creating the corresponding domain account. The administrator has been notified to resolve the problem.'
					return render(request, 'users/create_or_modify_user.html', dictionary)
			except Exception as e:
				dictionary['identity_service_available'] = False
				users_logger.error('There was a problem communicating with the identity service while attempting to modify a user. An exception was encountered: ' + type(e).__name__ + ' - ' + str(e))
				dictionary['warning'] = 'The user information was not modified because the identity service encountered a problem while creating the corresponding domain account. The administrator has been notified to resolve the problem.'
				return render(request, 'users/create_or_modify_user.html', dictionary)

		# Only save the user model for now, and wait to process the many-to-many relationships.
		# This way, many-to-many changes can be recorded.
		# See this web page for more information:
		# https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
		user = form.save(commit=False)
		user.save()
		record_active_state(request, user, form, 'is_active', user_id == 'new')
		record_local_many_to_many_changes(request, user, form, 'qualifications')
		record_local_many_to_many_changes(request, user, form, 'physical_access_levels')
		record_local_many_to_many_changes(request, user, form, 'projects')
		form.save_m2m()

		message = f"{user} has been added successfully to {site_title}" if user_id == 'new' else f"{user} has been updated successfully"
		messages.success(request, message)
		return redirect('users')
	else:
		return HttpResponseBadRequest('Invalid method')


@staff_member_required
@require_http_methods(['GET', 'POST'])
def deactivate(request, user_id):
	dictionary = {
		'user_to_deactivate': get_object_or_404(User, id=user_id),
		'reservations': Reservation.objects.filter(user=user_id, cancelled=False, missed=False, end__gt=timezone.now()),
		'staff_charges': StaffCharge.objects.filter(customer=user_id, end=None),
		'tool_usage': UsageEvent.objects.filter(user=user_id, end=None).prefetch_related('tool'),
	}
	user_to_deactivate = dictionary['user_to_deactivate']
	if request.method == 'GET':
		return render(request, 'users/safe_deactivation.html', dictionary)
	elif request.method == 'POST':
		identity_service = get_identity_service()
		if identity_service.get('available', False):
			parameters = {
				'username': user_to_deactivate.username,
				'domain': user_to_deactivate.domain,
			}
			try:
				timeout = identity_service.get('timeout', 3)
				result = requests.delete(identity_service['url'], data=parameters, timeout=timeout)
				# If the delete succeeds, or the user is not found, then everything is ok.
				if result.status_code not in (HTTPStatus.OK, HTTPStatus.NOT_FOUND):
					users_logger.error(f'The identity service encountered a problem while attempting to delete a user. The HTTP error is {result.status_code}: {result.text}')
					dictionary['warning'] = 'The user information was not modified because the identity service could not delete the corresponding domain account. The administrator has been notified to resolve the problem.'
					return render(request, 'users/safe_deactivation.html', dictionary)
			except Exception as e:
				users_logger.error('There was a problem communicating with the identity service while attempting to delete a user. An exception was encountered: ' + type(e).__name__ + ' - ' + str(e))
				dictionary['warning'] = 'The user information was not modified because the identity service could not delete the corresponding domain account. The administrator has been notified to resolve the problem.'
				return render(request, 'users/safe_deactivation.html', dictionary)

		if request.POST.get('cancel_reservations') == 'on':
			# Cancel all reservations that haven't ended
			for reservation in dictionary['reservations']:
				reservation.cancelled = True
				reservation.cancellation_time = timezone.now()
				reservation.cancelled_by = request.user
				reservation.save()
		if request.POST.get('disable_tools') == 'on':
			# End all current tool usage
			for usage_event in dictionary['tool_usage']:
				if usage_event.tool.interlock and not usage_event.tool.interlock.lock():
					error_message = f"The interlock command for the {usage_event.tool} failed. The error message returned: {usage_event.tool.interlock.most_recent_reply}"
					users_logger.error(error_message)
				usage_event.end = timezone.now()
				usage_event.save()
		if request.POST.get('force_area_logout') == 'on':
			area_access = user_to_deactivate.area_access_record()
			if area_access:
				area_access.end = timezone.now()
				area_access.save()
		if request.POST.get('end_staff_charges') == 'on':
			# End a staff charge that the user might be performing
			staff_charge = user_to_deactivate.get_staff_charge()
			if staff_charge:
				staff_charge.end = timezone.now()
				staff_charge.save()
				try:
					area_access = AreaAccessRecord.objects.get(staff_charge=staff_charge, end=None)
					area_access.end = timezone.now()
					area_access.save()
				except AreaAccessRecord.DoesNotExist:
					pass
			# End all staff charges that are being performed for the user
			for staff_charge in dictionary['staff_charges']:
				staff_charge.end = timezone.now()
				staff_charge.save()
				try:
					area_access = AreaAccessRecord.objects.get(staff_charge=staff_charge, end=None)
					area_access.end = timezone.now()
					area_access.save()
				except AreaAccessRecord.DoesNotExist:
					pass
		user_to_deactivate.is_active = False
		user_to_deactivate.save()
		activity_entry = ActivityHistory()
		activity_entry.authorizer = request.user
		activity_entry.action = ActivityHistory.Action.DEACTIVATED
		activity_entry.content_object = user_to_deactivate
		activity_entry.save()

		message = f"{user_to_deactivate} has been successfully deactivated"
		messages.success(request, message)
		return redirect('users')


@staff_member_required
@require_POST
def reset_password(request, user_id):
	try:
		identity_service = get_identity_service()
		user = get_object_or_404(User, id=user_id)
		timeout = identity_service.get('timeout', 3)
		result = requests.post(urljoin(identity_service['url'], '/reset_password/'), {'username': user.username, 'domain': user.domain}, timeout=timeout)
		if result.status_code == HTTPStatus.OK:
			dictionary = {
				'title': 'Password reset',
				'heading': 'The account password was set to the default',
			}
		else:
			dictionary = {
				'title': 'Oops',
				'heading': 'There was a problem resetting the password',
				'content': 'The identity service returned HTTP error code {}. {}'.format(result.status_code, result.text),
			}
	except Exception as e:
		dictionary = {
			'title': 'Oops',
			'heading': 'There was a problem communicating with the identity service',
			'content': 'Exception caught: {}. {}'.format(type(e).__name__, str(e)),
		}
	return render(request, 'acknowledgement.html', dictionary)


@staff_member_required
@require_POST
def unlock_account(request, user_id):
	try:
		identity_service = get_identity_service()
		user = get_object_or_404(User, id=user_id)
		timeout = identity_service.get('timeout', 3)
		result = requests.post(urljoin(identity_service['url'], '/unlock_account/'), {'username': user.username, 'domain': user.domain}, timeout=timeout)
		if result.status_code == HTTPStatus.OK:
			dictionary = {
				'title': 'Account unlocked',
				'heading': 'The account is now unlocked',
			}
		else:
			dictionary = {
				'title': 'Oops',
				'heading': 'There was a problem unlocking the account',
				'content': 'The identity service returned HTTP error code {}. {}'.format(result.status_code, result.text),
			}
	except Exception as e:
		dictionary = {
			'title': 'Oops',
			'heading': 'There was a problem communicating with the identity service',
			'content': 'Exception caught: {}. {}'.format(type(e).__name__, str(e)),
		}
	return render(request, 'acknowledgement.html', dictionary)


@login_required
@require_http_methods(['GET', 'POST'])
def user_preferences(request):
	user: User = User.objects.get(pk=request.user.id)
	if request.method == 'POST':
		form = UserPreferencesForm(data=request.POST, instance=user.preferences)
		if form.is_valid():
			form.save()
			messages.success(request, "Your preferences have been saved")
	dictionary = {
		'user_preferences': user.get_preferences(),
	}
	return render(request, 'users/preferences.html', dictionary)


def get_identity_service():
	return getattr(settings, 'IDENTITY_SERVICE', {})