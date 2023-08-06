import requests


class WizataDSAPIClient:

    def __init__(self):
        self.domain = None
        self.user = None
        self.password = None

    def __url(self):
        return "https://" + self.user + ":" + self.password + "@" + self.domain + "/dsapi/"

    def __header(self):
        return {'Content-Type': 'application/json'}

    def __request_process(self, method, route):
        response = requests.request(method, self.__url() + "route", headers=self.__header())
        return response

    def get_ds_function(self):
        return self.__request_process("GET", "get_ds_function")
