from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = \
    [
        path('', views.index, name='index'),
        #url(r'^signup/$', views.signup, name='signup'),
        url(r'^signup/$', views.register, name='signup'),
        url(r'^home/$', views.userHome, name='home'),
        url(r'^instructions/(?P<tournament_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})$', views.instructions, name='instructions'),
        url(r'^tournament/(?P<tournament_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})$', views.tournamentView, name='tournament'),
        url(r'^games/(?P<qt_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})$', views.gamesView, name='games'),
        url(r'^gamesPreview/(?P<uq_id>[0-9a-f-]+)',  views.gamesPreview, name='preview'),
    ]