# Generated by Django 3.2.3 on 2022-09-17 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiniela', '0008_filled_field_userQuiniela'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='gameId',
            field=models.CharField(default='A1', max_length=20, null=True),
        ),
    ]
