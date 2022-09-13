from django.contrib import admin
from .models import Teams, Game, QuinielaTournament, Phases, UserQuiniela


class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'type')
    search_fields = ['name']

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'init_date', 'end_date', 'group')
    search_fields = ['name', 'group']
    

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'game', 'phase', 'winner')
    search_fields = ['id']
    model = Teams

    def game(self, obj):
        res = str(obj.teamA) + '-' + str(obj.teamB)
        return res

class PhasesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class UserQuinielaAdmin(admin.ModelAdmin):
    list_display = ('points', 'quiniela_fk', 'djuser_fk')


admin.site.register(Teams, TeamsAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(QuinielaTournament, TournamentAdmin)
admin.site.register(Phases, PhasesAdmin)
admin.site.register(UserQuiniela, UserQuinielaAdmin)