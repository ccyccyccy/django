# Generated by Django 2.0 on 2017-12-10 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='create_on',
            new_name='created_on',
        ),
    ]
