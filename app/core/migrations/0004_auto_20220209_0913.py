# Generated by Django 2.1.15 on 2022-02-09 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='usser',
            new_name='user',
        ),
    ]