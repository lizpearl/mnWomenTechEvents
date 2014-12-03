
import requests
import json
import datetime as dt
# from django.conf import settings
# settings.configure()
# import django
# django.setup()

# relative import might need to be fixed later
import techCalendar.local.apiKeys as ak
import techCalendar.models as tcm

#from requests_oauthlib import OAuth1

# >>> url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
# >>> auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET',
#                   'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
class EventbriteEvent:

    def __init__( self ):
        self.eventbriteHost = "http://www.eventbriteapi.com" 
        self.eventbriteGet = "/v3/events/search/"
        self.eventbriteGroups = { 'Geekettes' : 2850467571 ,
                         'Gr8Ladies' : 6848465013 }

    def makeEventbritePayload ( self, eventBriteId ): 
        return { 'organizer.id' : eventBriteId,
                 'venue.city' : "Minneapolis", 
                 'token':ak.eventbriteKey }



# Assumptions
# These groups don't have a lot of events to warrent a page limit
# Sample Url 
# https://api.meetup.com/2/events?group_urlname=Girl-Develop-It-Minneapolis&omit=venue,fee&key=<meetup key here>
    def storeEvents ( self ):
        eventbriteUrl = self.eventbriteHost + self.eventbriteGet

        # grab json from each meetup group
        # API only allows for one group to be requested at once
        for ( k, v ) in self.eventbriteGroups.items():
            payload = self.makeEventbritePayload ( v )
            r = requests.get ( eventbriteUrl, params=payload )

            eventbriteEvents = r.json()['events']
            #print eventbriteEvents
            for ev in eventbriteEvents:
                 print ev['resource_uri']
                 print ev['name']['text']
                 print ev['start']['utc']
                 print ev['end']['utc']
                 print ev['organizer']['name']

                 groupName = ev['organizer']['name']
            #     print ev['duration']
            #     print ev['name']

            #     startTimeUTC = ev['time']/1000
            #     endTimeUTC = (ev['time'] + ev['duration'])/1000
                 (tg, created) = tcm.TechGroup.objects.get_or_create( name = groupName )
            
                 (ce, created) = tcm.CalendarEvent.objects.get_or_create( group = tg,
                                                                     title = ev['name']['text'],
                                                                     start_datetime = ev['start']['utc'],
                                                                     end_datetime = ev['end']['utc'] ,
                                                                     link = ev['resource_uri'])


#if __name__ == __main__:
ebe = EventbriteEvent()
ebe.storeEvents()


