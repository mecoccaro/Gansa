from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from .formGames import GameFormGroups, GamesFormSet
from .models import *
import json
import logging
logger = logging.getLogger(__name__)

groupsIds = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


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
    tableHeaders = ['Equipo', 'G', 'P', 'E', 'Puntos']
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
        count = 0
        aux = 0
        for inner in body:
            for idx, res in enumerate(inner):
                if res['name'] == 'csrfmiddlewaretoken':
                    continue
                if (count == 0):
                    if aux <= 0:
                        phase = 'groups'
                        results[phase] = {}
                        aux +=1
                elif (count == 1):
                    if aux == 1:
                        phase = '8vos'
                        results[phase] = {}
                        aux +=1
                elif (count == 2):
                    if aux == 2:
                        phase = '4tos'
                        results[phase] = {}
                        aux +=1
                elif (count == 3):
                    if aux == 3:
                        phase = 'semi'
                        results[phase] = {}
                        aux +=1
                elif (count == 4):
                    if aux == 4:
                        phase = 'final'
                        results[phase] = {}
                        aux +=1
                elif (count == 5):
                    if aux == 5:
                        phase = 'goaler'
                        results[phase] = {}
                        aux +=1
                if res['name'] == 'gameId':
                    gameIds = res['value']
                    if gameIds not in results[phase]:
                        results[phase][gameIds] = {}
                    continue
                if count > 0 and res['name'] == 'winnerTeam' and phase != 'final':
                    insideArr = inner[idx+1]
                    gameIds = insideArr['value']
                    if gameIds not in results[phase]:
                        results[phase][gameIds] = {}
                    results[phase][gameIds]['winnerTeam'] = res['value']
                    continue
                if res['name'] == 'resA':
                    results[phase][gameIds]['teamA'] = res['value']
                    continue
                if res['name'] == 'resB':
                    results[phase][gameIds]['teamB'] = res['value']
                    continue
                if phase == 'final':
                    results[phase][gameIds]['winnerTeam'] = res['value']
                if res['name'] == 'goaler':
                    results[phase] = res['value']
            count += 1
        qualyTypes = []
        logger.info('Quiniela submitted')
        print(qt_id)
        print(json.dumps(results))
        for i in range(13):
            qualyTypes.append('q'+str(i))
        qualyTypes.append('semi1')
        qualyTypes.append('semi2')
        qualyTypes.append('final')
        for keys in results.keys():
            phase = keys
            if phase != 'goaler':
                for gameIds in results[phase].keys():
                    resA = results[phase][gameIds]['teamA']
                    resB = results[phase][gameIds]['teamB']
                    if len(resA) == 0:
                        resA = 0
                    elif len(resA) == 0:
                        resB = 0
                    if(phase == 'groups'): #groups
                        games = GameQuinielaGroups()
                        gameTeams = Game.objects.get(gameId=gameIds)
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
                        games.gameId = gameIds
                        games.save()
                    else: # qualy games
                        games = GameQuinielaQualify()
                        teamName = results[phase][gameIds]['winnerTeam']
                        if teamName:
                            winner = Teams.objects.get(name=teamName)
                        else:
                            winner = Teams.objects.get(name='None')
                        games.winner = winner
                        games.user_quiniela = userQuiniela
                        games.scoreA = resA
                        games.scoreB = resB
                        games.gameId = gameIds
                        games.save()
            else:
                userQuiniela.goaler = results['goaler']
                userQuiniela.filled = True
                userQuiniela.save()

        return HttpResponseRedirect('/quiniela/tournament/{}'.format(tournament.id))

    context = {
        'tournament': tournament, 'games': games, 'groupsIds': groupsIds,
        'th': tableHeaders, 'teamsGroups': teamsGroups
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