import uuid
from django.db import models
from django.contrib.auth.models import User as DJuser
from django.contrib.auth.forms import UserCreationForm

class Teams(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name

class QuinielaTournament(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    init_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ("family", "can access family tournaments"),
            ("edFriends", "can access edFriends tournaments"),
            ("meFriends", "can access meFriends tournaments"),
        )


class UserQuiniela(models.Model):
    points = models.FloatField()
    quiniela_fk = models.ForeignKey(QuinielaTournament, on_delete=models.CASCADE)
    djuser_fk = models.ForeignKey(DJuser, on_delete=models.CASCADE)


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teamA = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='gameTeamA')
    teamB = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='gameTeamB')
    scoreA = models.IntegerField(null=True)
    scoreB = models.IntegerField(null=True)
    date = models.DateField()
    phase = models.CharField(max_length=20, null=True)
    Tournament_fk = models.ForeignKey(QuinielaTournament, on_delete=models.CASCADE)
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE)


class GameQuinielaUser(models.Model):
    teamA = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='teamA')
    teamB = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='teamB')
    user_quiniela = models.ForeignKey(UserQuiniela, on_delete=models.CASCADE)
    game_tournament = models.ForeignKey(QuinielaTournament, on_delete=models.CASCADE)
    scoreA = models.IntegerField(null=False)
    scoreB = models.IntegerField(null=False)
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE)
    gameId = models.ForeignKey(Game, on_delete=models.CASCADE)