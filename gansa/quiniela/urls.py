from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = \
    [
        path('', views.index, name='index'),
        #url(r'^signup/$', views.signup, name='signup'),
        url(r'^signup/$', views.register, name='signup'),
        url(r'^home/$', views.userHome, name='home')
    ]