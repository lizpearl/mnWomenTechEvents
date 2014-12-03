# from tutorial
from django.conf.urls import patterns, url

from techCalendar import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)

