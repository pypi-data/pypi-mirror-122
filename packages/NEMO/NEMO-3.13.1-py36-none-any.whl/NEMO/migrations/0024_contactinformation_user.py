# Generated by Django 2.2.13 on 2020-09-17 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NEMO', '0023_badgereader'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactinformation',
            name='user',
            field=models.OneToOneField(blank=True, help_text='Select a user to associate with this contact. When set, this contact information will be shown instead of the user information on pages like tool details.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
