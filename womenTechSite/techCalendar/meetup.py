
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
class MeetupEvent:

    def __init__( self ):
        self.meetupApiHost = "http://api.meetup.com"
        self.eventGet = "/2/events"
        #self.meetupGroups = [ 'Girl-Develop-It-Minneapolis']

        # TODO; Make this configurable
        self.meetupGroups = [ 'Girl-Develop-It-Minneapolis', 'PyLadiesTC', \
        'Girls-in-Tech-Minneapolis', 'Twin-Cities-Visualization-Group']


    def makeMeetupPayload ( self, meetupGroupName ): 
        return { 'group_urlname':meetupGroupName, 
                'omit':'venue,fee', 'key':ak.meetupKey, 
                'fields':'timezone' }


# eventBriteHost = "http://www.eventbriteapi.com"
# eventBriteGet = "/v3/events/search/"
# eventBriteGroups = { 'Geekettes': 2850467571 }

# Assumptions
# These groups don't have a lot of events to warrent a page limit
# Sample Url 
# https://api.meetup.com/2/events?group_urlname=Girl-Develop-It-Minneapolis&omit=venue,fee&key=<meetup key here>
    def storeEvents ( self ):
        meetupUrl = self.meetupApiHost + self.eventGet

        # grab json from each meetup group
        # API only allows for one group to be requested at once
        for m in self.meetupGroups:
            payload = self.makeMeetupPayload(m)
            r = requests.get(meetupUrl, params=payload)

            meetupEvents = r.json()['results']
            for ev in meetupEvents:
                print ev['event_url']
                print ev['group']['name']
                print ev['time'] # milliseconds since the epoch
                print ev['timezone']
                print ev['duration']
                print ev['name']

                startTimeUTC = ev['time']/1000
                endTimeUTC = (ev['time'] + ev['duration'])/1000
                (tg, created) = tcm.TechGroup.objects.get_or_create( name = ev['group']['name'] )
            
                (ce, created) = tcm.CalendarEvent.objects.get_or_create( group = tg,
                                                                     title = ev['name'],
                                                                     start_datetime = dt.datetime.fromtimestamp(startTimeUTC),
                                                                     end_datetime = dt.datetime.fromtimestamp(endTimeUTC) ,
                                                                     link = ev['event_url'])


#if __name__ == __main__:
mue = MeetupEvent()
mue.storeEvents()


