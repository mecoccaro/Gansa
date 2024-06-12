from django.contrib import admin
from django.contrib.admin.models import LogEntry

from .models import Game, Phases, QuinielaTournament, Teams, UserQuiniela, GameQuinielaGroups


class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'type')
    search_fields = ['name']

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'init_date', 'end_date', 'group')
    search_fields = ['name', 'group']
    

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'gameId', 'date', 'game', 'phase', 'winner')
    search_fields = ['id']
    model = Teams

    def game(self, obj):
        res = str(obj.teamA) + '-' + str(obj.teamB)
        return res

class PhasesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class UserQuinielaAdmin(admin.ModelAdmin):
    list_display = ('points', 'quiniela_fk', 'djuser_fk', 'filled')

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message']
    list_filter = ['action_time', 'user', 'content_type', 'action_flag']
    search_fields = ['object_repr', 'change_message']
    readonly_fields = list_display
    can_delete = False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class GameQuinielaGroupsAdmin(admin.ModelAdmin):
    list_display = ('user', 'gameId', 'teamA', 'teamB', 'scoreA', 'scoreB', 'winner')
    list_filter = ['user_quiniela', 'gameId']

    def user(self, obj):
        return obj.user_quiniela.djuser_fk.username

    def game_id(self, obj):
        return obj.gameId

    def teamA(self, obj):
        game = Game.objects.get(gameId=obj.gameId)
        return game.teamA.name if game else 'N/A'

    def teamB(self, obj):
        game = Game.objects.get(gameId=obj.gameId)
        return game.teamB.name if game else 'N/A'

    def scoreA(self, obj):
        game = Game.objects.get(gameId=obj.gameId)
        return game.scoreA if game else 'N/A'

    def scoreB(self, obj):
        game = Game.objects.get(gameId=obj.gameId)
        return game.scoreB if game else 'N/A'

    def winner(self, obj):
        game = Game.objects.get(gameId=obj.gameId)
        return game.winner.name if game else 'N/A'


admin.site.register(GameQuinielaGroups, GameQuinielaGroupsAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(QuinielaTournament, TournamentAdmin)
admin.site.register(Phases, PhasesAdmin)
admin.site.register(UserQuiniela, UserQuinielaAdmin)
admin.site.register(LogEntry, LogEntryAdmin)