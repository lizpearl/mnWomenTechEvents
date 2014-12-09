import requests
import json
import datetime as dt

import techCalendar.local.apiKeys as ak
import techCalendar.models as tcm


class EventSite(object):

    """
    Base cal
    """

    # groupDict is a dictionary of key value pairs
    def __init__(self, host, apiGetEvents, groupDict={},
                 groupType=tcm.CalendarEvent.NONE):
        self.host = host
        self.apiGetEvents = apiGetEvents
        self.groupDict = groupDict
        self.groupUrl = self.host + self.apiGetEvents
        self.groupType = groupType

    def makeParamPayload(self, groupId, rangeStart=None):
        print "EventSite:makeParamPayload called"
        print "Need to implement this function for child class"

    def storeEvents(self):
        for (k, v) in self.groupDict.items():
            self.storeGroupEvents(v)

    def storeGroupEvents(self, groupId):
        # Set up to only get events after the latest
        # timestamp but since this calendar isn't
        # time critical, just get all events again

        latestCreated = None

        payload = self.makeParamPayload(groupId,
                                        rangeStart=latestCreated)
        r = requests.get(self.groupUrl, params=payload)
        print r.url

        if (r.status_code == requests.codes.ok):
            return self.parseEvents(r)

    # Returns number of created events for testing
    def parseEvents(self, response):
        print "EventSite:parseEvent called"
        print "Need to implement this function for child class"
