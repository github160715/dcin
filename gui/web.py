import requests
import dateutil.parser as parser
from datetime import datetime


class Web:
# TODO адрес веб-службы задается в conf файле
    def __init__(self):
        
        self.agents_url = "http://localhost:3000/handlers/agents/"
        self.status_url = "http://localhost:3000/handlers/status/"
        self.last_url = "http://localhost:3000/handlers/last_info/"
        self.info_url = "http://localhost:3000/handlers/info/"

    def get_agents(self):

        r = requests.get(self.agents_url)
        return r.json()

    def get_status(self):

        r = requests.get(self.status_url)
        return r.json()

    def get_last(self):

        r = requests.get(self.last_url)
        return r.json()

    def get_info(self, beg, end):

        r = requests.get(self.info_url + parser.parse(str(beg)).isoformat() + "/" + parser.parse(str(end)).isoformat())
        return r.json()

    def date_validator(self, date):
        try:
            parser.parse(date).isoformat()
            return True
        except ValueError:
            return False

if __name__ == '__main__':

#    print(Web().get_info(datetime(2015, 7, 22, 10, 22, 57, 48000), datetime(2015, 7, 30, 10, 22, 57, 48000)))
     print(Web().get_info("2015-07-21T07:25:10.658Z", "2015-07-30T08:05:59.658Z"))
