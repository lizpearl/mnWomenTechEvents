
import requests
import json
import datetime as dt

import techCalendar.local.apiKeys as ak
import techCalendar.models as tcm


class EventbriteEvent:

    def __init__(self):
        self.eventbriteHost = "http://www.eventbriteapi.com"
        self.eventbriteGet = "/v3/events/search/"
        self.eventbriteGroups = {'Geekettes': 2850467571,
                                 'Gr8Ladies': 6848465013,
                                 'OpenTwinCities': 31452055}

    def makeEventbritePayload(self, eventBriteId):

        # Assumptions: Some groups are nationals so use venue city as
        # Minneapolis as a filter. This should probably be changed to
        # something more general since events might be held in
        # St. Paul or the suburbs

        return {'organizer.id': eventBriteId,
                'venue.city': "Minneapolis",
                'token': ak.eventbriteKey}


# Assumptions
# These groups don't have a lot of events to warrant a page limit
# Sample Url
# https://api.meetup.com/2/events?group_urlname=Girl-Develop-It-Minneapolis&omit=venue,fee&key=<meetup
# key here>
    def storeEvents(self):
        eventbriteUrl = self.eventbriteHost + self.eventbriteGet

        # grab json from each meetup group
        # API only allows for one group to be requested at once
        for (k, v) in self.eventbriteGroups.items():
            payload = self.makeEventbritePayload(v)
            r = requests.get(eventbriteUrl, params=payload)

            eventbriteEvents = r.json()['events']
            for ev in eventbriteEvents:
                self.storeSingleEvent(ev)

    # Need sample single event info here
    def storeSingleEvent(self, eventBriteEvent):

        # Need a try/catch here
        eventUrl = ev['url']
        eventTitle = ev['name']['text']
        eventStart = ev['start']['utc']
        eventEnd = ev['end']['utc']
        eventGroup = ev['organizer']['name']

        (tg, created) = tcm.TechGroup.objects.get_or_create(
            name=eventGroup)

        (ce, created) = tcm.CalendarEvent.objects.get_or_create(
            group=tg,
            title=eventTitle,
            start_datetime=eventStart,
            end_datetime=eventEnd,
            link=eventUrl)


if __name__ == '__main__':
    ebe = EventbriteEvent()
    ebe.storeEvents()
