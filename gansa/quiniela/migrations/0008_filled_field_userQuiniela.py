# Generated by Django 3.2.3 on 2022-09-17 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiniela', '0007_deleted_unnecessary_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='userquiniela',
            name='filled',
            field=models.BooleanField(default=False),
        ),
    ]
