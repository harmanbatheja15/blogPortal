# Generated by Django 4.1 on 2022-09-03 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_rename_body_article_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publish_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
