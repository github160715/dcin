import json
import daemon
import sys
import os
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


def execution(agents, period):
    with daemon.DaemonContext(working_directory=os.path.dirname(os.path.abspath(__file__)), stdout=sys.stdout, stderr=sys.stderr):
        while True:
            for agent in agents:
                agent.get_data()
            sleep(period)

if __name__ == "__main__":
    confs = get_conf()
    period = confs["period"]
    agents = create_agents(confs)

    while True:
        try:
            execution(agents, period)
        except:
            continue
    # execution()
    # with daemon.DaemonContext(working_directory='/home/mikhail/working/PycharmProjects/server', stdout=sys.stdout, stderr=sys.stderr):
    #     confs = get_conf()
    #     period = confs["period"]
    #     agents = create_agents(confs)
    #     while True:
    #         for agent in agents:
    #             agent.get_data()
    #         sleep(period)
    # agents, period = create_agents(get_conf())
    #
    # while True:
    #     for agent in agents:
    #         agent.get_data()
    #     sleep(period)

    # try:
    #     with daemon.DaemonContext(working_directory='/home/mikhail/PycharmProjects/server', stdout=sys.stdout, stderr=sys.stderr):
    #         confs = get_conf()
    #         period = confs["period"]
    #         raise KeyError
    #         agents = create_agents(confs)
    #         while True:
    #             for agent in agents:
    #                 agent.get_data()
    #             sleep(period)
    # except:
    #     print("asda")
    # with daemon.DaemonContext(working_directory='/home/mikhail/PycharmProjects/server', stdout=sys.stdout, stderr=sys.stderr):
    #
    #     try:
    #         confs = get_conf()
    #         period = confs["period"]
    #         raise KeyError
    #         agents = create_agents(confs)
    #         while True:
    #             for agent in agents:
    #                 agent.get_data()
    #             sleep(period)
    #     except:
    #         sys.exit(1)
