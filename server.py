#!/usr/bin/python3

import json
import daemon
import os
from classes import Agent
from time import sleep

# "chmod +x server.py" - make executable
# ./server.py run executable
# Работает как демон, чтобы увидеть его "ps -x", чтобы выключить "sudo kill -9 pid"

def create_agents(conf):
    list_of_agents = []
    for key in conf["agents"]:
        list_of_agents.append(Agent(key, conf["agents"][key], conf["error_file"]))

    return list_of_agents


def get_conf():
    with open("conf.json") as conf_file:
        return json.load(conf_file)


def execution(agents, period):
    with daemon.DaemonContext(working_directory=os.path.dirname(os.path.abspath(__file__))):
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
