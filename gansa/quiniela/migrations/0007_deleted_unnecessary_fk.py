# Generated by Django 3.2.3 on 2022-09-15 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiniela', '0006_tournament_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamequinielagroups',
            name='game_tournament',
        ),
        migrations.RemoveField(
            model_name='gamequinielaqualify',
            name='game_tournament',
        ),
    ]
