import requests
import json
import dateutil.parser as parser
from datetime import datetime


class Agent:

    def __init__(self, agents, urls, periods, info, ids):
        self.agents = agents
        self.urls = urls
        self.info = info
        self.periods = periods
        self.ids = ids


class Web:
# TODO адрес веб-службы задается в conf файле
    def __init__(self):

        self.url = "http://localhost:3000/"
        self.agents_url = self.url + "handlers/agents/"
        self.status_url = self.url + "handlers/status/"
        self.last_url = self.url + "handlers/last_info/"
        self.info_url = self.url + "handlers/info/"
        self.add_url = self.url + "add"
        self.del_url = self.url + "del"
        self.upd_url = self.url + "upd"

    def get_all(self):

        r = requests.get(self.agents_url)
        return r.json()

    def get_agents_and_statuses(self):

        agents = []
        statuses = {}

        for agent in self.get_all():
            agents.append(agent["name"])
            if agent["status"]:
                statuses[agent["name"]] = "on"
            else:
                statuses[agent["name"]] = "off"

        return agents, statuses

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

    def create_agent(self):
        data = []
        agents = []
        urls = []
        periods = []
        ids = {}

        all_info = self.get_all()

        for agent in all_info:
            data.append([agent["name"], agent["http"], agent["period"]])
            agents.append(agent["name"])
            urls.append(agent["http"])
            periods.append(agent["period"])
            ids[agent["name"]] = agent["_id"]

        return Agent(agents, urls, periods, data, ids)

    def add_agent(self, name, url, period):
        data = {
            "name": name,
            "http": url,
            "period": period,
            "status": False,
            "last": ""
        }

        headers = {'content-type': 'application/json'}
        response = requests.post(self.add_url, data=json.dumps(data), headers=headers)

    def delete_agent(self, idx):

        data = {
            "_id": idx
        }

        headers = {'content-type': 'application/json'}
        response = requests.post(self.del_url, data=json.dumps(data), headers=headers)

    def modify_agent(self, idx, name, url, period):
        data = {
            "_id": idx,
            "name": name,
            "http": url,
            "period": period,
        }

        headers = {'content-type': 'application/json'}
        response = requests.post(self.upd_url, data=json.dumps(data), headers=headers)

if __name__ == '__main__':
    pass
#    print(Web().get_info(datetime(2015, 7, 22, 10, 22, 57, 48000), datetime(2015, 7, 30, 10, 22, 57, 48000)))
  #   print(Web().get_info("2015-07-21T07:25:10.658Z", "2015-07-30T08:05:59.658Z"))
    print(Web().get_agents())

