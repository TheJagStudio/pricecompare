# Generated by Django 3.1 on 2022-08-14 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userhistory',
            old_name='rh',
            new_name='lh',
        ),
    ]
