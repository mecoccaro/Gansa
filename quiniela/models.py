import uuid
from django.db import models
from django.contrib.auth.models import User as DJuser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as DJuser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    GROUPS = (
        ('F', 'family'),
        ('EF', 'edFriends'),
        ('MF', 'meFriends'),
        ('N', 'none')
    )
    group = models.CharField(max_length=2, choices=GROUPS, default='N')

    class Meta:
        managed = True
        permissions = (
            ("family", "can access family tournaments"),
            ("edFriends", "can access edFriends tournaments"),
            ("meFriends", "can access meFriends tournaments"),
        )

    def __str__(self):
        return self.name


class UserQuiniela(models.Model):
    points = models.FloatField()
    goaler = models.TextField(null=True)
    filled = models.BooleanField(default=False, null=False)
    quiniela_fk = models.ForeignKey(QuinielaTournament, on_delete=models.CASCADE)
    djuser_fk = models.ForeignKey(DJuser, on_delete=models.CASCADE)


class Phases(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teamA = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='gameTeamA')
    teamB = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='gameTeamB')
    scoreA = models.IntegerField(null=True)
    scoreB = models.IntegerField(null=True)
    date = models.DateField()
    phase = models.ForeignKey(Phases, on_delete=models.CASCADE)
    Tournament_fk = models.ForeignKey(QuinielaTournament, on_delete=models.CASCADE)
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE)
    gameId = models.CharField(max_length=20, null=True, default='A1')


class GameQuinielaGroups(models.Model):
    user_quiniela = models.ForeignKey(UserQuiniela, on_delete=models.CASCADE)
    scoreA = models.IntegerField(null=False)
    scoreB = models.IntegerField(null=False)
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE)
    gameId = models.CharField(max_length=20, null=True)

class GameQuinielaQualify(models.Model):
    user_quiniela = models.ForeignKey(UserQuiniela, on_delete=models.CASCADE)
    scoreA = models.IntegerField(null=False)
    scoreB = models.IntegerField(null=False)
    teamA = models.CharField(max_length=100, null=True)
    teamB = models.CharField(max_length=100, null=True)
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE)
    gameId = models.CharField(max_length=20, null=True)

@receiver(post_save, sender=Game)
def calc_points(sender, instance, **kwargs):
    gameId = instance.gameId
    scoreA = instance.scoreA
    scoreB = instance.scoreB
    winner = instance.winner
    playersGames = GameQuinielaGroups.objects.filter(gameId=gameId)
    for game in playersGames:
        print(game.scoreA)
        uqt = UserQuiniela.objects.get(id=game.user_quiniela.id)
        puntos = 0
        if winner == game.winner:
            puntos += 3
        if game.scoreA == scoreA:
            puntos += 1
        if game.scoreB == scoreB:
            puntos += 1
        uqt.points += puntos
        uqt.save()