# Generated by Django 4.1 on 2022-09-03 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_blogcomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogcomment',
            old_name='sno',
            new_name='id',
        ),
    ]
