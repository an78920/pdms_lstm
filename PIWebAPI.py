from requests_ntlm import HttpNtlmAuth
import requests
import json

import urllib3

urllib3.disable_warnings()


class Connector:
    def __init__(self, end_point, user, password):
        self._url = None
        self._end_point = end_point
        self._user = user
        self._password = password

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = self._end_point + value

    def query(self):
        requests.packages.urllib3.disable_warnings()
        if self._url is None:
            resp = requests.get(self._end_point, auth=HttpNtlmAuth(self._user, self._password), verify=False)
        else:
            resp = requests.get(self._url, auth=HttpNtlmAuth(self._user, self._password), verify=False)
        return resp.json()


class Interpolated(Connector):
    def __init__(self, end_point, user, password, webid):
        super().__init__(end_point, user, password)
        self._webId = webid
        self._startTime = None
        self._endTime = None
        self._interval = None
        self.build_url()

    def build_url(self):
        parameter_list = []

        if self._startTime is not None:
            parameter_list.append('startTime=' + self._startTime)

        if self._endTime is not None:
            parameter_list.append('endTime=' + self._endTime)

        if self._interval is not None:
            parameter_list.append('interval=' + self._interval)

        if self._maxCount is not None:
            parameter_list.append('maxCount=' + self._maxCount)

        parameter = '&'.join(parameter_list)
        interpolated_url = '/streams/%s/interpolated?%s' % (self._webId, parameter)
        super(Interpolated, Interpolated).url.__set__(self, interpolated_url)

    @property
    def startTime(self):
        return self._startTime

    @startTime.setter
    def startTime(self, value):
        self._startTime = value
        self.build_url()

    @property
    def endTime(self):
        return self._endTime

    @endTime.setter
    def endTime(self, value):
        self._endTime = value
        self.build_url()

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        self._interval = value
        self.build_url()


class GetRecorded(Connector):
    def __init__(self, end_point, user, password, webid):
        super().__init__(end_point, user, password)
        self._webId = webid
        self._startTime = None
        self._endTime = None
        self._maxCount = None
        self.build_url()

    def build_url(self):
        parameter_list = []

        if self._startTime is not None:
            parameter_list.append('startTime=' + self._startTime)

        if self._endTime is not None:
            parameter_list.append('endTime=' + self._endTime)

        if self._maxCount is not None:
            parameter_list.append('maxCount=' + self._maxCount)

        parameter = '&'.join(parameter_list)
        recorded_url = '/streams/%s/recorded?%s' % (self._webId, parameter)
        super(GetRecorded, GetRecorded).url.__set__(self, recorded_url)

    @property
    def startTime(self):
        return self._startTime

    @startTime.setter
    def startTime(self, value):
        self._startTime = value
        self.build_url()

    @property
    def endTime(self):
        return self._endTime

    @endTime.setter
    def endTime(self, value):
        self._endTime = value
        self.build_url()

    @property
    def maxCount(self):
        return self._maxCount

    @maxCount.setter
    def maxCount(self, value):
        self._maxCount = str(value)
        self.build_url()


class GetValue(Connector):
    def __init__(self, end_point, user, password, webid):
        super().__init__(end_point, user, password)
        self._webId = webid
        self.build_url()

    def build_url(self):
        get_value_url = '/streams/%s/value' % (self._webId)
        super(GetValue, GetValue).url.__set__(self, get_value_url)


class GetSummary(Connector):
    def __init__(self, end_point, user, password, webid):
        super().__init__(end_point, user, password)
        self._webId = webid
        self._startTime = None
        self._endTime = None
        self._summaryDuration = None
        self._summaryType = None
        self.build_url()

    def build_url(self):
        parameter_list = []

        if self._startTime is not None:
            parameter_list.append('startTime=' + self._startTime)

        if self._endTime is not None:
            parameter_list.append('endTime=' + self._endTime)

        if self._summaryDuration is not None:
            parameter_list.append('summaryDuration=' + self._summaryDuration)

        if self._summaryType is not None:
            parameter_list.append('summaryType=' + self._summaryType)

        parameter = '&'.join(parameter_list)
        summary_url = '/streams/%s/summary?%s' % (self._webId, parameter)
        super(GetSummary, GetSummary).url.__set__(self, summary_url)

    @property
    def startTime(self):
        return self._startTime

    @startTime.setter
    def startTime(self, value):
        self._startTime = value
        self.build_url()

    @property
    def endTime(self):
        return self._endTime

    @endTime.setter
    def endTime(self, value):
        self._endTime = value
        self.build_url()

    @property
    def summaryDuration(self):
        return self._summaryDuration

    @summaryDuration.setter
    def summaryDuration(self, value):
        self._summaryDuration = value
        self.build_url()

    @property
    def summaryType(self):
        return self._summaryType

    @summaryType.setter
    def summaryType(self, value):
        self._summaryType = value
        self.build_url()


def get_webid(endpoint, user, password, webapi, tag):
    url = '%s/points?path=\\%s\%s' % (endpoint, webapi, tag)
    resp = requests.get(url, auth=HttpNtlmAuth(user, password), verify=False)
    return resp.json()['WebId']


END_POINT = 'https://192.168.10.12/piwebapi/'
USER = 'piuser'
PASSWORD = 'piuser'
WEB_ID = 'F1DPqdt6BsThFU-w3NhPIcyHDwAwAAAAUEktSURFU1xDRFQxNTg'


def test():
    inter = GetSummary(END_POINT, USER, PASSWORD, WEB_ID)
    inter.startTime = '*-4d'
    inter.endTime = '*-3d'
    inter.summaryDuration = '6h'
    inter.summaryType = 'Average'
    print(json.dumps(inter.query(), indent=4))

    get_value = GetValue(END_POINT, USER, PASSWORD, WEB_ID)
    print(json.dumps(get_value.query(), indent=4))


if __name__ == '__main__':
    test()
