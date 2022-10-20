from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from .formGames import GameFormGroups, GamesFormSet
from .models import QuinielaTournament, Teams, UserQuiniela, Game, GameQuinielaGroups, GameQuinielaQualify
import json


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
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request, 'Account was created for ' + user)
        return redirect('/accounts/login')
    else:
        print('Form is not valid')
        messages.error(request, 'Error Processing Your Request')
        context = {'form': form}
        return render(request, 'registration/signup.html', context)

    return render(request, 'registration/signup.html', {})

def userHome(request):
    famTournament = QuinielaTournament.objects.filter(group = 'F')
    efTournament = QuinielaTournament.objects.filter(group = 'EF')
    tournament = QuinielaTournament.objects.all
    teams = Teams.objects.all
    context = {'tournament': tournament, 'famtournament': famTournament, 'teams': teams}
    return render(request, 'home.html', context)


def tournamentView(request, tournament_id):
    try:
        tournament = QuinielaTournament.objects.get(id=tournament_id)
    except:
        raise Http404("Tournament does not exist")
    users = UserQuiniela.objects.filter(quiniela_fk=tournament_id).order_by('-points')
    context = {'tournament': tournament, 'user': users}
    return render(request, 'user/tournament.html', context)


def gamesView(request, qt_id):
    formset = GamesFormSet()
    if request.method == 'GET':
        form = GameFormGroups()
        context = {'form': form, 'qt_id': qt_id}
        return render(request, 'games/gameInput.html', context)

    if request.method == 'POST':
        form = GameFormGroups(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully saved form')
        return redirect('/quiniela/home')
    else:
        print('Form is not valid')
        messages.error(request, 'Error Processing Your Request')
        context = {'form': form}
        return render(request, '/quiniela/home', context)

    return render(request, '/quiniela/home', {})


def gamesView2(request, qt_id):
    groupsIds = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    tableHeaders = ['Equipo', 'G', 'P', 'E', 'Puntos']
    try:
        tournament = QuinielaTournament.objects.get(id=qt_id)
        games = Game.objects.filter(Tournament_fk=qt_id)
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
            if res['name'] == 'gameId':
                gameIds = res['value']
                results[gameIds] = {}
            if res['name'] == 'resA':
                results[gameIds]['teamA'] = res['value']
            if res['name'] == 'resB':
                results[gameIds]['teamB'] = res['value']
        print(results)
        for keys in results.keys():
            gameGroups = GameQuinielaGroups()
            gameTeams = Game.objects.get(gameId=keys)
            teamA = Teams.objects.get(name=gameTeams.teamA.name)
            teamB = Teams.objects.get(name=gameTeams.teamB.name)
            tie = Teams.objects.get(name='None')
            resA = results[keys]['teamA']
            resB = results[keys]['teamB']
            gameGroups.user_quiniela = userQuiniela
            gameGroups.scoreA = resA
            gameGroups.scoreB = resB
            gameGroups.gameId = keys
            if  resA > resB:
                gameGroups.winner = teamA
            elif resB > resA:
                gameGroups.winner = teamB
            else:
                gameGroups.winner = tie
            gameGroups.save()
        return redirect('tournament', tournament_id=qt_id)

    context = {
        'tournament': tournament, 'games': games, 'groupsIds': groupsIds,
        'th': tableHeaders, 'teamsGroups': teamsGroups
        }
    return render(request, 'games/gameInput.html', context)