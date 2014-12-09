
import requests
import json
import datetime as dt

import techCalendar.eventSite as es
import techCalendar.local.apiKeys as ak
import techCalendar.models as tcm


class EventbriteEvent(es.EventSite):

    def __init__(self):

        eventbriteGroups = {'Geekettes': 2850467571,
                            'Gr8Ladies': 6848465013,
                            'OpenTwinCities': 5847915855}

        super(EventbriteEvent, self).__init__(
            host="http://www.eventbriteapi.com",
            apiGetEvents="/v3/events/search/",
            groupDict=eventbriteGroups,
            groupType=tcm.CalendarEvent.EVENTBRITE)

    def makeParamPayload(self, groupId, rangeStart=None):

        # Assumptions: Some groups are nationals so use venue city as
        # Minneapolis as a filter. This should probably be changed to
        # something more general since events might be held in
        # St. Paul or the suburbs

        payload = {'organizer.id': groupId,
                   'venue.city': "Minneapolis",
                   'token': ak.eventbriteKey}
        if rangeStart:
            payload['date_created.range_start'] = rangeStart

        return payload

    def parseEvents(self, response):
        createdEvents = 0
        eventbriteEvents = (response.json()).get('events', [])
        for ev in eventbriteEvents:
            # Need a try/catch here to handle missing information
            eventUrl = ev['url']
            eventTitle = ev['name']['text']
            eventStart = ev['start']['utc']
            eventEnd = ev['end']['utc']
            eventGroup = ev['organizer']['name']
            eventCreated = ev['created']

            (tg, created) = tcm.TechGroup.objects.get_or_create(
                name=eventGroup)

            (ce, created) = tcm.CalendarEvent.objects.get_or_create(
                group=tg,
                title=eventTitle,
                start_datetime=eventStart,
                end_datetime=eventEnd,
                link=eventUrl,
                source=tcm.CalendarEvent.EVENTBRITE,
                created_datetime=eventCreated)
            createdEvents += created
        return createdEvents


if __name__ == '__main__':
    ebe = EventbriteEvent()
    ebe.storeEvents()

# Sample Query
# https://www.eventbriteapi.com/v3/events/search/?token=<token here>&organizer.id=2850467571&venue.city=Minneapolis
# {
#     "pagination": {
#         "object_count": 1,
#         "page_number": 1,
#         "page_size": 50,
#         "page_count": 1
#     },
#     "events": [
#         {
#             "resource_uri": "https://www.eventbriteapi.com/v3/events/14035581803/",
#             "name": {
#                 "text": "Twin Cities Geekettes: A Day in the Life of a Geekette",
#                 "html": "Twin Cities Geekettes: A Day in the Life of a Geekette"
#             },
#             "description": {
#                 "text": "Twin Cities Geekettes: A Day in the Life of a Geekette \nWe are excited to announce that starting in December, CoCo Coworking Space\u00a0will be partnering with\u00a0the\u00a0Twin Cities Geekettes\u00a0to provide us a place to gather on a monthly basis. Our goal is to have a more regular time and place to meet. For our first monthly gathering on December 10th, we will feature our members by offering a round of lightning talks related to the theme \"A Day in the Life of a Geekette.\" Come check out the new digs, have a bite to eat, and get to know your fellow Geekettes! \nAgenda \n6:00 PM - 6:25 PM: Gather and network \n6:25 PM - 6:30 PM: Geekettes opening remarks \n6:30 PM - 8:15 PM: Lightning talks \n6:30: Caroline Karanja - Product development and creative initiatives in a Start up  6:45: Jasmine Russell - A Day in the Life of a Digital Analyst  7:00: Jennifer Simon - A Day in the Life of a Geekette\u00a0- Networking 101  7:15: Anna Bliss - Yes, Mom, the Theater Major Was Useful  7:30: Mary Jenn -\u00a0Uniting, Growing & Supporting the Female Developer Community in the Twin Cites  7:45: Allison Figus -\u00a0Grails-debug: A day in the life of a Groovy/Grails programmer  8:00: Roxanne Johnson -\u00a0A Day in the Life of a Research Analyst: Becoming your Organization's go-to Geek(ette) \n8:15 PM - 8:30 PM: Questions, network, wrap-up \nWe are looking for lightning talk presenters! \nWe want our events to feature our Geekette community, so we invite YOU to give a 5-10 minute lightning talk in the theme of \"A Day in the Life of a Geekette\". If you've never done one before, it's a great way to try your hand at public speaking in a low-stress environment. Lightning talks are also a great tool to have in your back pocket for when you're at a conference and a random lightning talk session pops up on the schedule. If you don't know what a lightning talk is, go check out this awesome lightning talk on giving lightning talks. \nIf you are interested, please send a talk title (in the theme of \"A Day in the Life of a Geekette\" to jenna@geekettes.io. Example titles: \"A Day in the Life of a User Experience Designer at Company XYZ\", \"Recruiter by Day, Wannabe Progremmer by Night\", \"Why I Identify as a Geekette\". \nMeet our Twin Cities Geekettes Ambassadors:  \n \nPlease visit: http://www.geekettes.io/cities/twincities/ambassadors \nParking \nStreet parking is available on residential streets south of Lake St. You can also park in the Calhoun Square Ramp and get the $6.50 CoCo Guest rate (ask CoCo Community Manager on duty for parking validation). \nGuests of CoCo cannot park in the CVS parking lot. Vehicles will be towed. \n---- \n*Special thanks to our host and sponsors:",
# "html": "<P><IMG SRC=\"https://evbdn.eventbrite.com/s3-s3/eventlogos/44206609/tcbanner.png\" ALT=\"\" WIDTH=\"500\" HEIGHT=\"185\"><\/P>\r\n<P><SPAN STYLE=\"font-size: large;\"><SPAN STYLE=\"line-height: 28.799999237060547px;\"><STRONG>Twin Cities Geekettes: A Day in the Life of a Geekette<\/STRONG><\/SPAN><\/SPAN><\/P>\r\n<P><SPAN STYLE=\"line-height: 1.6em;\">We are excited to announce that starting in December, <A STYLE=\"font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 20.7999992370605px;\" TITLE=\"CoCo Coworking Space\" HREF=\"http://cocomsp.com/\" REL=\"nofollow\">CoCo Coworking Space<\/A>\u00a0will be partnering with\u00a0the\u00a0<\/SPAN><A STYLE=\"font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 20.7999992370605px;\" HREF=\"https://www.facebook.com/twincitiesgeekettes\" REL=\"nofollow\">Twin Cities Geekettes<\/A><SPAN STYLE=\"line-height: 1.6em;\">\u00a0to provide us a place to gather on a monthly basis. Our goal is to have a more regular time and place to meet. For our first monthly gathering on December 10th, we will feature our members by offering a round of lightning talks related to the theme \"A Day in the Life of a Geekette.\" Come check out the new digs, have a bite to eat, and get to know your fellow Geekettes!<\/SPAN><\/P>\r\n<P><SPAN STYLE=\"line-height: 1.6em;\"><STRONG>Agenda<\/STRONG><\/SPAN><\/P>\r\n<P><SPAN STYLE=\"line-height: 1.6em;\">6:00 PM - 6:25 PM: Gather and network<\/SPAN><\/P>\r\n<P><SPAN STYLE=\"line-height: 1.6em;\">6:25 PM - 6:30 PM: Geekettes opening remarks<\/SPAN><\/P>\r\n<P><SPAN STYLE=\"line-height: 1.6em;\">6:30 PM - 8:15 PM: Lightning talks<\/SPAN><\/P>\r\n<P STYLE=\"padding-left: 30px;\"><SPAN STYLE=\"line-height: 1.6em;\"><SPAN STYLE=\"font-stretch: normal; font-size: 13px; font-family: Arial;\">6:30: Caroline Karanja - Product development and creative initiatives in a Start up<\/SPAN><BR> <SPAN STYLE=\"font-stretch: normal; font-size: 13px; font-family: Arial;\">6:45: Jasmine Russell - A Day in the Life of a Digital Analyst<\/SPAN><BR> <SPAN STYLE=\"font-stretch: normal; font-size: 13px; font-family: Arial;\">7:00: Jennifer Simon - A Day in the Life of a Geekette\u00a0- Networking 101<\/SPAN><BR> <SPAN STYLE=\"font-stretch: normal; font-size: 13px; font-family: Arial;\">7:15: Anna Bliss - Yes, Mom, the Theater Major Was Useful<\/SPAN><BR> <SPAN STYLE=\"font-stretch: normal; font-size: 13px; font-family: Arial;\">7:30: Mary Jenn -\u00a0<\/SPAN><SPAN STYLE=\"font-stretch: normal; font-size: 13px; font-family: Helvetica;\">Uniting, Growing &amp; Supporting the Female Developer Community in the Twin Cites<\/SPAN><BR> <SPAN STYLE=\"font-stretch: normal; font-size: 13px; font-family: Arial;\">7:45: Allison Figus -\u00a0Grails-debug: A day in the life of a Groovy/Grails programmer<\/SPAN><BR> <SPAN STYLE=\"font-stretch: normal; font-size: 13px; font-family: Arial;\">8:00: Roxanne Johnson -\u00a0<\/SPAN><SPAN STYLE=\"font-stretch: normal; font-size: 13px; font-family: Helvetica;\">A Day in the Life of a Research Analyst: Becoming your Organization's go-to Geek(ette)<\/SPAN><\/SPAN><\/P>\r\n<P><SPAN STYLE=\"line-height: 1.6em;\">8:15 PM - 8:30 PM: Questions, network, wrap-up<\/SPAN><\/P>\r\n<P><STRONG><SPAN STYLE=\"font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; line-height: 20.7999992370605px;\">We are looking for lightning talk presenters!<\/SPAN><\/STRONG><\/P>\r\n<P><SPAN STYLE=\"line-height: 1.6em;\">We want our events to feature our Geekette community, so we invite YOU to give a 5-10 minute lightning talk in the theme of \"A Day in the Life of a Geekette\". If you've never done one before, it's a great way to try your hand at public speaking in a low-stress environment. Lightning talks are also a great tool to have in your back pocket for when you're at a conference and a random lightning talk session pops up on the schedule. If you don't know what a lightning talk is, go check out <A TITLE=\"How to Give a Lightning Talk\" HREF=\"http://vimeo.com/57965823\" REL=\"nofollow\">this awesome lightning talk on giving lightning talks<\/A>.<\/SPAN><\/P>\r\n<P><SPAN><EM><SPAN STYLE=\"line-height: 1.6em;\">If you are interested, please send a talk title (in the theme of \"A Day in the Life of a Geekette\" to <A TITLE=\"jenna@geekettes.io\" HREF=\"mailto:jenna@geekettes.io\" REL=\"nofollow\">jenna@geekettes.io<\/A>. Example titles: \"A Day in the Life of a User Experience Designer at Company XYZ\", \"Recruiter by Day, Wannabe Progremmer by Night\", \"Why I Identify as a Geekette\".<\/SPAN><\/EM><\/SPAN><\/P>\r\n<P><SPAN STYLE=\"line-height: 1.6em;\"><STRONG>Meet our Twin Cities Geekettes Ambassadors:<\/STRONG><BR><\/SPAN><\/P>\r\n<P><IMG SRC=\"https://cdn.evbuc.com/eventlogos/109565585/screenshot20141029at10.15.16pm.png\" ALT=\"\" WIDTH=\"500\" HEIGHT=\"172\"><\/P>\r\n<P><SPAN STYLE=\"font-family: arial, helvetica, sans-serif;\"><SPAN STYLE=\"line-height: 1.6em;\">Please visit: <A TITLE=\"Twin Cities Geekettes - Ambassadors\" HREF=\"http://www.geekettes.io/cities/twincities/ambassadors\" REL=\"nofollow\">http://www.geekettes.io/cities/twincities/ambassadors<\/A><\/SPAN><\/SPAN><\/P>\r\n<P STYLE=\"margin: 0px 0px 18px; padding: 0px; color: rgba(0, 0, 0, 0.670588); font-family: Whitney, helvetica, arial, sans-serif; font-size: 15px; line-height: 21px;\"><SPAN STYLE=\"font-size: small; font-family: arial, helvetica, sans-serif; color: #000000;\"><STRONG>Parking<\/STRONG><\/SPAN><\/P>\r\n<P STYLE=\"margin: 0px 0px 18px; padding: 0px; color: rgba(0, 0, 0, 0.670588); font-family: Whitney, helvetica, arial, sans-serif; font-size: 15px; line-height: 21px;\"><SPAN STYLE=\"font-family: arial, helvetica, sans-serif; font-size: small; color: #000000;\">Street parking is available on residential streets south of Lake St. You can also park in the Calhoun Square Ramp and get the $6.50 CoCo Guest rate (ask CoCo Community Manager on duty for parking validation).<\/SPAN><\/P>\r\n<P STYLE=\"margin: 0px 0px 18px; padding: 0px; color: rgba(0, 0, 0, 0.670588); font-family: Whitney, helvetica, arial, sans-serif; font-size: 15px; line-height: 21px;\"><SPAN STYLE=\"font-family: arial, helvetica, sans-serif; font-size: small; color: #000000;\">Guests of CoCo <STRONG>cannot<\/STRONG> park in the CVS parking lot. Vehicles will be towed.<\/SPAN><\/P>\r\n<P STYLE=\"margin: 0px 0px 18px; padding: 0px; color: rgba(0, 0, 0, 0.670588); font-family: Whitney, helvetica, arial, sans-serif; font-size: 15px; line-height: 21px;\"><SPAN STYLE=\"line-height: 1.6em; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 13px; color: #000000;\">----<\/SPAN><\/P>\r\n<P><SPAN STYLE=\"font-family: arial, helvetica, sans-serif; font-size: medium;\"><EM><STRONG>*Special thanks to our host and sponsors:\u00a0<\/STRONG><\/EM><\/SPAN><\/P>\r\n<P><SPAN STYLE=\"font-family: arial, helvetica, sans-serif; font-size: medium;\"><EM><STRONG><A HREF=\"http://cocomsp.com/\" REL=\"nofollow\"><IMG TITLE=\"CoCo\" SRC=\"https://cdn.evbuc.com/eventlogos/109565585/cocodarkred500px9.44.46am.jpg\" ALT=\"CoCo\" WIDTH=\"150\"><\/A>\u00a0 \u00a0 \u00a0<\/STRONG><\/EM>\u00a0\u00a0<EM><STRONG><A HREF=\"http://www.612softwarefoundry.com\" REL=\"nofollow\"><IMG TITLE=\"612 Software Foundry\" SRC=\"https://cdn.evbuc.com/eventlogos/109565585/612softwarefoundrytwitternotagline.png\" ALT=\"612 Software Foundry\" WIDTH=\"150\"><\/A><\/STRONG><\/EM><\/SPAN><\/P>"
#             },
#             "logo": {
#                 "id": "8865591",
#                 "url": "http://cdn.evbuc.com/images/8865591/91794689151/1/logo.png"
#             },
#             "id": "14035581803",
#             "url": "http://www.eventbrite.com/e/twin-cities-geekettes-a-day-in-the-life-of-a-geekette-registration-14035581803?aff=ebapi",
#             "logo_url": "http://cdn.evbuc.com/images/8865591/91794689151/1/logo.png",
#             "start": {
#                 "timezone": "America/Chicago",
#                 "local": "2014-12-10T18:00:00",
#                 "utc": "2014-12-11T00:00:00Z"
#             },
#             "end": {
#                 "timezone": "America/Chicago",
#                 "local": "2014-12-10T20:30:00",
#                 "utc": "2014-12-11T02:30:00Z"
#             },
#             "created": "2014-10-30T03:05:34Z",
#             "changed": "2014-12-09T16:34:05Z",
#             "capacity": 45,
#             "status": "live",
#             "currency": null,
#             "online_event": null,
#             "organizer_id": "2850467571",
#             "venue_id": "8842575",
#             "category_id": "102",
#             "subcategory_id": "2999",
#             "format_id": "10",
#             "organizer": {
#                 "description": {
#                     "text": null,
#                     "html": null
#                 },
#                 "logo": {
#                     "id": "7131327",
#                     "url": "http://cdn.evbuc.com/images/7131327/44516055263/2/logo.jpg"
#                 },
#                 "resource_uri": "https://www.eventbriteapi.com/v3/organizers/2850467571/",
#                 "id": "2850467571",
#                 "name": "Geekettes ",
#                 "url": "http://www.eventbrite.com/o/geekettes-2850467571",
#                 "num_past_events": 49,
#                 "num_future_events": 2
#             },
#             "venue": {
#                 "address": {
#                     "address_1": "1010 W Lake St",
#                     "address_2": "Suite 100",
#                     "city": "Minneapolis",
#                     "region": "MN",
#                     "postal_code": "55408",
#                     "country": "US",
#                     "latitude": "44.94891450000001",
#                     "longitude": "-93.29275630000001"
#                 },
#                 "resource_uri": "https://www.eventbriteapi.com/v3/venues/8842575/",
#                 "id": "8842575",
#                 "name": "CoCo Coworking and Collaborative Space - Uptown",
#                 "latitude": "44.94891450000001",
#                 "longitude": "-93.29275630000001"
#             },
#             "category": {
#                 "resource_uri": "https://www.eventbriteapi.com/v3/categories/102/",
#                 "id": "102",
#                 "name": "Science & Technology",
#                 "name_localized": "Science & Technology",
#                 "short_name": "Science & Tech",
#                 "short_name_localized": "Science & Tech"
#             },
#             "subcategory": {
#                 "resource_uri": "https://www.eventbriteapi.com/v3/subcategories/2999/",
#                 "id": "2999",
#                 "name": "Other"
#             },
#             "format": {
#                 "resource_uri": "https://www.eventbriteapi.com/v3/formats/10/",
#                 "id": "10",
#                 "name": "Meeting or Networking Event",
#                 "name_localized": "Meeting or Networking Event",
#                 "short_name": "Networking",
#                 "short_name_localized": "Networking"
#             },
#             "ticket_classes": [
#                 {
#                     "resource_uri": "https://www.eventbriteapi.com/v3/events/14035581803/ticket_classes/30429129/",
#                     "id": "30429129",
#                     "name": "RSVP",
#                     "description": null,
#                     "donation": false,
#                     "free": true,
#                     "minimum_quantity": 1,
#                     "maximum_quantity": null,
#                     "event_id": "14035581803"
#                 }
#             ]
#         }
#     ]
# }
