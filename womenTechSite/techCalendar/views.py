from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from techCalendar.models import CalendarEvent


# Create your views here.
def index(request):
    events_list = CalendarEvent.objects.all()
    template = loader.get_template('techCalendar/index.html')
    context = RequestContext ( request ,
        { 'events_list': events_list, 
        })
    return HttpResponse(template.render(context))

# Taken from stackoverflow
def eventsFeed(request):
    from django.utils.timezone import utc
    from django.core.serializers.json import DjangoJSONEncoder

    if request.is_ajax():
        print 'Its ajax from fullCalendar()'

    try:
        start = datetime.fromtimestamp(int(request.GET.get('start', False))).replace(tzinfo=utc)
        end = datetime.fromtimestamp(int(request.GET.get('end',False)))
    except ValueError:
        start = datetime.now.replace(tzinfo=utc)
        end = start + timedelta(days=7)

    entries = CalendarEvents.objects.filter(date__gte=start).filter(date__lte=end)
    print entries
    json_list = []
    for entry in entries:
        id = entry.id
        title = entry.title
        start = entry.date.strftime("%Y-%m-%dT%H:%M:%S")
        allDay = False

        json_entry = {'id':id, 'start':start, 'allDay':allDay, 'title': title}
        json_list.append(json_entry)

    return HttpResponse(json.dumps(json_list), content_type='application/json')
