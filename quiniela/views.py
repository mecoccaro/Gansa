import json
import logging
import os

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .formGames import GameFormGroups, GamesFormSet
from .forms import RegisterForm, CustomPasswordResetForm
from .models import *

logger = logging.getLogger(__name__)

groupsIds = ['A', 'B', 'C', 'D', 'E', 'F']  # Extend to G H or more groups if necessary
INFO = 1001


def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, '500.html')
    response.status_code = 500
    return response


def index(request):
    return HttpResponse("Gansa. Propiedad de gansa 2022.")

def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'registration/signup.html', context)

    if request.method == 'POST':
        form = RegisterForm(request.POST)

    if form.is_valid():
        usrQ = UserQuiniela()
        quiniela = QuinielaTournament.objects.get(id='51c4a49d-6f00-4e6d-8359-45281949ea3c')  # main tournament
        userCreated = form.save()
        us = User.objects.get(id=userCreated.id)
        user = form.cleaned_data.get('username')
        messages.success(request, 'Account was created for ' + user)
        group = Group.objects.get(name='Family')
        userCreated.groups.add(group)
        usrQ.djuser_fk = us
        usrQ.quiniela_fk = quiniela
        usrQ.points = 0
        usrQ.save()
        return redirect('/accounts/login')
    else:
        print('Form is not valid')
        messages.error(request, 'Error Processing Your Request')
        context = {'form': form}
        return render(request, 'registration/signup.html', context)

    return render(request, 'registration/signup.html', {})

def userHome(request):
    famTournament = QuinielaTournament.objects.filter(group='F')
    efTournament = QuinielaTournament.objects.filter(group='EF')
    tournament = QuinielaTournament.objects.all
    teams = Teams.objects.all
    context = {'tournament': tournament, 'famtournament': famTournament, 'teams': teams}
    return render(request, 'home.html', context)


def tournamentView(request, tournament_id):
    try:
        tournament = QuinielaTournament.objects.get(id=tournament_id)
        userQuiniela = UserQuiniela.objects.get(quiniela_fk=tournament_id, djuser_fk=request.user)
    except:
        raise Http404("Tournament does not exist")
    users = UserQuiniela.objects.filter(quiniela_fk=tournament_id).order_by('-points')
    context = {
        'tournament': tournament, 
        'user': users,
        'userQuiniela': userQuiniela}
    return render(request, 'user/tournament.html', context)


def gamesView(request, qt_id):
    tableHeaders = ['Equipo', 'G', 'P', 'E', 'Puntos', 'GF', 'GC', 'GD']

    try:
        tournament = QuinielaTournament.objects.get(id=qt_id)
        games = Game.objects.filter(Tournament_fk=qt_id).order_by('gameId')
        userQuiniela = UserQuiniela.objects.get(quiniela_fk=qt_id, djuser_fk=request.user)
    except Exception as e:
        raise Http404("Tournament does not exist: {}".format(e))
    
    teamsGroups = []
    for g in groupsIds:
        gg = []
        gGames = Game.objects.filter(gameId__contains=g)
        for game in gGames:
            if game.teamA.name not in gg:
                gg.append(game.teamA.name)
            if game.teamB.name not in gg:
                gg.append(game.teamB.name)
        teamsGroups.append(gg)

    if request.method == 'POST':
        body = json.loads(request.body)
        results = {}
        for res in body:
            resA = res['scoreA']
            resB = res['scoreB']
            if res['phase'] == 'groups':
                games = GameQuinielaGroups()
                gameTeams = Game.objects.get(gameId=res['gameId'])
                teamA = Teams.objects.get(name=gameTeams.teamA.name)
                teamB = Teams.objects.get(name=gameTeams.teamB.name)
                tie = Teams.objects.get(name='None')
                if  resA > resB:
                    games.winner = teamA
                elif resB > resA:
                    games.winner = teamB
                else:
                    games.winner = tie
                games.user_quiniela = userQuiniela
                games.scoreA = resA
                games.scoreB = resB
                games.gameId = res['gameId']
                games.save()
            else:
                games = GameQuinielaQualify()
                teamName = res['winner']
                teamNA = res['teamA']
                teamNB = res['teamB']
                if teamName:
                    winner = Teams.objects.get(name=teamName)
                else:
                    winner = Teams.objects.get(name='None')
                games.winner = winner
                games.user_quiniela = userQuiniela
                games.scoreA = resA
                games.scoreB = resB
                games.gameId = res['gameId']
                games.teamA = res['teamA']
                games.teamB = res['teamB']
                games.save()
            if (res['phase'] == 'final'):
                userQuiniela.goaler = res['goaler']
                userQuiniela.filled = True
                userQuiniela.save()
        return HttpResponseRedirect(reverse('preview', kwargs={'uq_id': userQuiniela.id}))

    context = {
        'tournament': tournament, 'games': games, 'groupsIds': groupsIds,
        'th': tableHeaders, 'teamsGroups': teamsGroups, 'user_quiniela': userQuiniela.id
        }
    return render(request, 'games/gameInput.html', context)

def gamesPreview(request, uq_id):
    try:
        groupGames = GameQuinielaGroups.objects.filter(user_quiniela_id=uq_id)
        qualy = GameQuinielaQualify.objects.filter(user_quiniela_id=uq_id)
        userQuiniela = UserQuiniela.objects.get(id=uq_id)
    except Exception as e:
        raise Http404("Games not found: {}".format(e))
    games = {}
    for g in groupGames:
        game = Game.objects.get(gameId=g.gameId)
        games[g.gameId] = {}
        games[g.gameId]['teamA'] = game.teamA.name
        games[g.gameId]['teamB'] = game.teamB.name
        games[g.gameId]['resA'] = g.scoreA
        games[g.gameId]['resB'] = g.scoreB
    
    context = {
        'tournament_id': userQuiniela.quiniela_fk_id,
        'groups': groupGames,
        'qualy': qualy,
        'games': games,
        'groupsIds': groupsIds,
        'goaler': userQuiniela.goaler
        }
    return render(request, 'games/gamesPreview.html', context)

def instructions(request, tournament_id):
    try:
        tournament = QuinielaTournament.objects.get(id=tournament_id)
        userQuiniela = UserQuiniela.objects.get(quiniela_fk=tournament_id, djuser_fk=request.user)
    except:
        raise Http404("Tournament does not exist")
    users = UserQuiniela.objects.filter(quiniela_fk=tournament_id).order_by('-points')
    context = {
        'tournament': tournament, 
        'user': users,
        'userQuiniela': userQuiniela,
        'tabla': userQuiniela.quiniela_fk_id}
    return render(request, 'user/instructions.html', context)

def analysis(request, tournament_id):
    try:
        tournament = QuinielaTournament.objects.get(id=tournament_id)
        userQuiniela = UserQuiniela.objects.get(quiniela_fk=tournament_id, djuser_fk=request.user)
    except:
        raise Http404("Tournament does not exist")
    users = UserQuiniela.objects.filter(quiniela_fk=tournament_id).order_by('-points')
    dataUrl = os.environ.get('DATA')
    context = {
        'tournament': tournament, 
        'user': users,
        'userQuiniela': userQuiniela,
        'tabla': userQuiniela.quiniela_fk_id,
        'data': dataUrl
    }
    return render(request, 'user/analysis.html', context)


def custom_password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            return redirect(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
    else:
        form = CustomPasswordResetForm()
    return render(request, 'registration/custom_password_reset.html', {'form': form})

def custom_password_reset_confirm(request, uidb64=None, token=None):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)  # Opcional, para mantener la sesión iniciada
                messages.success(request, 'Tu contraseña ha sido restablecida exitosamente.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
    else:
        messages.error(request, 'El enlace de restablecimiento de contraseña no es válido.')
        return redirect('custom_password_reset')
    return render(request, 'registration/custom_password_confirm.html', {'form': form})