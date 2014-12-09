import requests
import json
import datetime as dt

import techCalendar.local.apiKeys as ak
import techCalendar.models as tcm


class EventSite(object):

    def __init__(self, host, apiGetEvents, groupDict={}):
        self.host = host
        self.apiGetEvents = apiGetEvents
        self.groupDict = groupDict
        self.groupUrl = self.host + self.apiGetEvents

    def makeParamPayload(self, groupId):
        print "EventSite:makeParamPayload called"
        print "Need to implement this function for child class"

    def storeEvents(self):
        for (k, v) in self.groupDict.items():
            self.storeGroupEvents(v)

    def storeGroupEvents(self, groupId):
        payload = self.makeParamPayload(groupId)
        r = requests.get(self.groupUrl, params=payload)

        if (r.status_code == requests.codes.ok):
            return self.parseEvents(r)

    # Returns number of created events for testing
    def parseEvents(self, response):
        print "EventSite:parseEvent called"
        print "Need to implement this function for child class"
