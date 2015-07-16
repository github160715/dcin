import json
import daemon
from classes import Agent
from time import sleep


def create_agents(conf):
    list_of_agents = []
    for key in conf["agents"]:
        list_of_agents.append(Agent(key, conf["agents"][key], conf["error_file"]))

    return list_of_agents


def get_conf():
    with open("conf.json") as conf_file:
        return json.load(conf_file)

if __name__ == "__main__":
    # agents, period = create_agents(get_conf())
    #
    # while True:
    #     for agent in agents:
    #         agent.get_data()
    #     sleep(period)

    with daemon.DaemonContext(working_directory='/home/mikhail/PycharmProjects/server'):
        confs = get_conf()
        period = confs["period"]
        agents = create_agents(confs)
        while True:
            for agent in agents:
                agent.get_data()
            sleep(period)
