from django.contrib import admin
from techCalendar.models import TechGroup
from techCalendar.models import CalendarEvent

# Register your models here.
admin.site.register(TechGroup)
admin.site.register(CalendarEvent)