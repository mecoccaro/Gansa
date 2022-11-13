from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory

from .models import (GameQuinielaGroups, GameQuinielaQualify,
                     QuinielaTournament, Teams, UserQuiniela)


class GameFormGroups(forms.Form):
    scoreA = forms.IntegerField(max_value=100, min_value=0, required=True)
    scoreB = forms.IntegerField(max_value=100, min_value=0, required=True)
    winnerId = forms.CharField(max_length=20)
    user_quiniela_id = forms.UUIDField(required=True)
    winner_id = forms.UUIDField(required=True)

    class Meta:
        model = GameQuinielaGroups
        fields = ['scoreA', 'scoreB', 'winnerId', 'user_quiniela_id', 'winner_id']

GamesFormSet = formset_factory(GameFormGroups, extra=64)
