from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from techCalendar.models import CalendarEvent


# Create your views here.
def index(request):
    events_list = CalendarEvent.objects.order_by( 'start_datetime' )
    template = loader.get_template('techCalendar/index.html')
    context = RequestContext ( request ,
        { 'events_list': events_list, 
        })
    return HttpResponse(template.render(context))

