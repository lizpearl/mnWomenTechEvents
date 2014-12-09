from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from techCalendar.models import CalendarEvent
import techCalendar.meetup as tcm
import techCalendar.eventbrite as tce


# Create your views here.
def index(request):

    # Probably not the place for this
    # It's also slow....
    mue = tcm.MeetupEvent()
    mue.storeEvents()

    ebe = tce.EventbriteEvent()
    ebe.storeEvents()

    events_list = CalendarEvent.objects.order_by('start_datetime')
    template = loader.get_template('techCalendar/index.html')
    context = RequestContext(request,
                             {'events_list': events_list,
                              })
    return HttpResponse(template.render(context))
