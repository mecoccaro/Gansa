import uuid
from django.db import models
from django.contrib.auth.models import User as DJuser
from django.contrib.auth.forms import UserCreationForm

class Tournament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    init_date = models.DateField()
    end_date = models.DateField()


class Quiniela(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    init_date = models.DateField()
    end_date = models.DateField()
    tournament_fk = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class UserQuiniela(models.Model):
    points = models.FloatField()
    quiniela_fk = models.ForeignKey(Quiniela, on_delete=models.CASCADE)
    djuser_fk = models.ForeignKey(DJuser, on_delete=models.CASCADE)


class Teams(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=10, null=True)


class Game(models.Model):
    teamA = models.CharField(max_length=50)
    teamB = models.CharField(max_length=50)
    date = models.DateField()
    phase = models.CharField(max_length=20, null=True)
    Tournament_fk = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class GameQuinielaUser(models.Model):
    teamA = models.CharField(max_length=50)
    teamB = models.CharField(max_length=50)
    user_quiniela = models.ForeignKey(UserQuiniela, on_delete=models.CASCADE)
    scoreA = models.IntegerField(null=False)
    scoreB = models.IntegerField(null=False)