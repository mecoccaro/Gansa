# Generated by Django 3.2.3 on 2022-09-06 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiniela', '0005_tournament_perm_managed'),
    ]

    operations = [
        migrations.AddField(
            model_name='quinielatournament',
            name='group',
            field=models.CharField(choices=[('F', 'family'), ('EF', 'edFriends'), ('MF', 'meFriends'), ('N', 'none')], default='N', max_length=2),
        ),
    ]
