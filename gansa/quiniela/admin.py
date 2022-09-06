from django.contrib import admin
from .models import Teams, Game, QuinielaTournament, Phases


class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'type')
    search_fields = ['name']

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'init_date', 'end_date')
    search_fields = ['name']
    

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'game', 'phase', 'winner')
    search_fields = ['id']
    model = Teams

    def game(self, obj):
        res = str(obj.teamA) + '-' + str(obj.teamB)
        return res

class PhasesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Teams, TeamsAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(QuinielaTournament, TournamentAdmin)
admin.site.register(Phases, PhasesAdmin)