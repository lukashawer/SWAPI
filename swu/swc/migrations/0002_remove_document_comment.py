# Generated by Django 3.2.3 on 2022-03-13 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='comment',
        ),
    ]