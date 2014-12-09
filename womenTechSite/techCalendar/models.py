from django.db import models

# Create your models here.


class TechGroup(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, null=True)

    def __str__(self):
        return '%s' % (self.name)


class CalendarEvent (models.Model):

    NONE = 0
    MEETUP = 1
    EVENTBRITE = 2

    source = (
        (NONE, 'None'),
        (MEETUP, 'Meetup'),
        (EVENTBRITE, 'EventBrite'),
    )

    group = models.ForeignKey(TechGroup)
    title = models.CharField(max_length=512)
    start_datetime = models.DateTimeField('start_datetime')
    end_datetime = models.DateTimeField('end_datetime')
    link = models.CharField(max_length=2048)
    source = models.IntegerField(default=NONE)
    created_datetime = models.DateTimeField('created_datetime')

    def __str__(self):
        return '%s %s' % (self.group.name, self.title)
