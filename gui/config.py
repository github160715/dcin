import json


def get_conf():

    with open("../server/conf.json") as conf_file:

        return json.load(conf_file)


class Agent:

    def __init__(self, agents, urls, periods, info):
        self.agents = agents
        self.urls = urls
        self.info = info
        self.periods = periods


class Config:

    def __init__(self):
        self.conf = get_conf()

    def get_agents_info(self):
        info = []
        agents = []
        urls = []
        periods = []

        self.conf = get_conf()

        for item in self.conf["agents"]:
            info.append([item[0], item[1], item[2]])
            agents.append(item[0])
            urls.append(item[1])
            periods.append(item[2])

        return Agent(agents, urls, periods, info)

    def dump(self):
        try:
            with open("../server/conf.json", 'w') as f:
                json.dump(self.conf, f)

        except OSError: # parent of IOError, OSError *and* WindowsError where available
            print("Can't open server/conf.json")
    def change_agent(self, index, name, url, period):
        self.conf = get_conf()

        old_name = self.conf["agents"][index][0]

        self.conf["agents"][index][0] = name
        self.conf["agents"][index][1] = url
        self.conf["agents"][index][2] = period

        if old_name != name:
            self.conf["agents"][index].extend((old_name, "modify"))

        self.dump()

    def add_agent(self, name, url, period):
        self.conf = get_conf()

        self.conf["agents"].append([name, url, period])

        self.dump()

    def delete_agent(self, index):
        self.conf = get_conf()

        self.conf["agents"][index].append("delete")

        self.dump()

if __name__ == '__main__':

    Config().get_agents_info()



