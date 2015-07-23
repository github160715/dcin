#!/usr/bin/env python3 

import json
import daemon
import os
import re
from sys import argv
from classes import Agent
from time import sleep
from urllib import request

# "chmod +x server.py" - make executable
# ./server.py - run executable
# Работает как демон, чтобы увидеть его "ps -x", чтобы выключить "sudo kill -9 pid"

global last_modified


def check_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not re.match(regex, url) or url[-1] != '/':
        raise ValueError

def create_agents(conf):
    list_of_agents = []
    for item in conf["agents"]:
        if len(item) != 3:
            continue
        check_url(item[1])
        list_of_agents.append(Agent(item[0], item[1], conf["error_file"]))

    return list_of_agents


def get_conf():
    with open("conf.json") as conf_file:
        return json.load(conf_file)


def execution(agents, period):
    global last_modified
    with daemon.DaemonContext(working_directory=os.path.dirname(os.path.abspath(__file__))):
        while True:
            for agent in agents:
                agent.get_data()
            sleep(period)

            modified = update_time('conf.json')
            if modified > last_modified:
                print("changed")
                last_modified = modified

                try:
                    confs = get_conf()
                    period = confs["period"]
                    agents = create_agents(confs)
                except ValueError:
                    continue

def update_time(filename):
    return os.path.getmtime(filename)


if __name__ == "__main__":

    last_modified = update_time('conf.json')
    print(last_modified)

    os.chdir(os.path.dirname(argv[0]))
    confs = get_conf()
    period = confs["period"]
    agents = create_agents(confs)

    while True:
        try:
            execution(agents, period)
        except:
            continue
