
import requests
import json
import datetime as dt

import techCalendar.local.apiKeys as ak
import techCalendar.models as tcm


class MeetupEvent:

    def __init__(self):
        self.meetupApiHost = "http://api.meetup.com"
        self.eventGet = "/2/events"

        # TODO; Make this configurable
        self.meetupGroups = ['Girl-Develop-It-Minneapolis', 'PyLadiesTC',
                             'Girls-in-Tech-Minneapolis', 'Twin-Cities-Visualization-Group',
                             'OpenTwinCities']

    def makeMeetupPayload(self, meetupGroupName):
        return {'group_urlname': meetupGroupName,
                'omit': 'venue,fee', 'key': ak.meetupKey,
                'fields': 'timezone'}

    # Sample Url
    # https://api.meetup.com/2/events?group_urlname=Girl-Develop-It-Minneapolis&omit=venue,fee&key=<meetup
    # key here>
    def storeEvents(self):
        meetupUrl = self.meetupApiHost + self.eventGet

        # grab json from each meetup group
        # API only allows for one group to be requested at once
        for m in self.meetupGroups:
            payload = self.makeMeetupPayload(m)
            r = requests.get(meetupUrl, params=payload)

            meetupEvents = r.json()['results']

            # need to do checks for
            for ev in meetupEvents:
                self.storeSingleEvent(ev)

    def storeSingleEvent(self, meetupEvent):

        # Need a try/catch here
        eventUrl = ev['event_url']
        eventGroup = ev['group']['name']
        eventStart = ev['time']  # milliseconds since the epoch
        eventTimeZone = ev['timezone']
        eventDuration = ev['duration']
        eventTitle = ev['name']
        eventCreated = ev['created']

        startTimeUTC = eventStart / 1000
        endTimeUTC = (eventStart + eventDuration) / 1000
        createdTimeUTC = eventCreated / 1000
        (tg, created) = tcm.TechGroup.objects.get_or_create(
            name=ev['group']['name'])

        (ce, created) = tcm.CalendarEvent.objects.get_or_create(
            group=tg,
            title=eventTitle,
            start_datetime=dt.datetime.fromtimestamp(startTimeUTC),
            end_datetime=dt.datetime.fromtimestamp(endTimeUTC),
            link=eventUrl,
            source=tcm.CalendarEvent.MEETUP,
            created_datetime=dt.datetime.fromtimestamp(createdTimeUTC))


if __name__ == '__main__':
    mue = MeetupEvent()
    mue.storeEvents()

# API call and response
# https://api.meetup.com/2/events?group_urlname=Girl-Develop-It-Minneapolis&omit=venue,fee&key=<meetup key here>
# {"results":[{"status":"upcoming","visibility":"public","maybe_rsvp_count":0,"utc_offset":-21600000,"id":"218917557","duration":7200000,"time":1418860800000,"waitlist_count":0,"announced":true,"updated":1418059448000,"created":1417044292000,"yes_rsvp_count":47,"event_url":"http:\/\/www.meetup.com\/Girl-Develop-It-Minneapolis\/events\/218917557\/","description":"<p>Come meet other Girl Develop It Minneapolis members at Bauhaus Brew Labs, a brewery in NE Minneapolis that recently launched after a successful <a href=\"https:\/\/www.kickstarter.com\/projects\/2091293866\/bauhaus-brew-labs-its-time-to-build-a-brewing-wund\">kickstarter campaign<\/a>.  Share and celebrate your accomplishments during this year (perhaps like making your first web page!?!) and then stick around for <a href=\"http:\/\/triviamafia.com\/bauhaus\/\">trivia<\/a> starting at 8pm.<\/p> <p>Everyone is welcome to attend.  If you're new to the group, come find out what GDI is all about.   <\/p> <p><img src=\"http:\/\/photos1.meetupstatic.com\/photos\/event\/7\/f\/f\/e\/600_431912766.jpeg\" \/><\/p> <p>Girl Develop It is a national nonprofit with 45 chapters representing 29,000 members.<\/p> <p>Questions or Comments? Email lizl@girldevelopit.com.<\/p>","headcount":0,"name":"Holiday Mixer","group":{"id":14070112,"created":1398287644000,"group_lat":44.939998626708984,"name":"Girl Develop It Minneapolis","group_lon":-93.25,"join_mode":"open","urlname":"Girl-Develop-It-Minneapolis","who":"Nerdettes"}},{"rsvp_limit":60,"status":"upcoming","visibility":"public","maybe_rsvp_count":0,"utc_offset":-21600000,"id":"219078943","duration":7200000,"time":1421281800000,"waitlist_count":0,"announced":true,"updated":1417824191000,"created":1417756655000,"yes_rsvp_count":5,"event_url":"http:\/\/www.meetup.com\/Girl-Develop-It-Minneapolis\/events\/219078943\/","description":"<p><b>Part One: Q &amp; A: Your Questions Answered About the Recruiting Process<\/b><\/p> <p>Participants will hear about the process of working with a staffing firm, and learn the pros of working with one. We will open the floor to questions after a quick run-down of Apex and how we find top-notch candidates for our Fortune 500 clients.<\/p> <p><b>Part Two: Your Professional Profile-- How to Create the Most Effective Resume<\/b><\/p> <p>We will dissect common IT related resumes received, and advise on how to spruce them up to catch the eye of the hiring manager. Participants are encouraged to bring their own resumes, and will receive one-on-one time with the instructors.<\/p> <p><b>Part Three: Interviews and Negotiating the Offer <\/b><\/p> <p>Preparation is key to a good interview. We will provide you with practical information on preparing for, and understanding the important steps of a job interview. After you've aced the interview and receive an offer, it's important to take the time to carefully evaluate the offer so you are making an educated decision to accept, or to reject. The last thing you want to do is to make a hasty decision that you will regret later on.<\/p>","headcount":0,"name":"IT Career Workshop with Apex Systems","group":{"id":14070112,"created":1398287644000,"group_lat":44.939998626708984,"name":"Girl Develop It Minneapolis","group_lon":-93.25,"join_mode":"open","urlname":"Girl-Develop-It-Minneapolis","who":"Nerdettes"}}],"meta":{"lon":"","count":2,"link":"https:\/\/api.meetup.com\/2\/events","next":"","total_count":2,"url":"https:\/\/api.meetup.com\/2\/events?key=563122302c1d381924771f443338162c&omit=venue%2Cfee&status=upcoming&order=time&limited_events=False&group_urlname=Girl-Develop-It-Minneapolis&desc=false&offset=0&format=json&page=200&fields=","id":"","title":"Meetup Events v2","updated":1418059448000,"description":"Access Meetup events using a group, member, or event id. Events in private groups are available only to authenticated members of those groups. To search events by topic or location, see [Open Events](\/meetup_api\/docs\/2\/open_events).","method":"Events","lat":""}}
