# Generated by Django 3.1.4 on 2021-05-06 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210504_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
