#!/usr/bin/env python3

import os
import json, requests, sys, pymongo
from threading import Thread, Event
from pymongo import MongoClient
from daemon3x import daemon
from datetime import datetime
from time import sleep

db = MongoClient().test


class Thr(Thread):
    def __init__(self, event, doc):
        Thread.__init__(self)
        self.stopped = event
        self.doc = doc

    def run(self):
        while not self.stopped.wait(self.doc['period']):
            try:
                cpu = (requests.get(self.doc['http'] + '/vals/cpu')).json()
                mem = (requests.get(self.doc['http'] + '/vals/memory')).json()

                t = datetime.strptime(cpu['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
                res = {
                    "agent": self.doc['name'],
                    "time": t,
                    "cpu": cpu["cpu"],
                    "total": mem["total"],
                    "used": mem["used"],
                }

                try:
                    db.agents.update_one(
                        {"_id" : self.doc["_id"]},
                        {"$set": {"last": t,
                              "status": True}})
                    db.states.insert_one(res)

                except pymongo.errors.PyMongoError:
                    print("mongo error")

            except requests.RequestException:

                try:
                    db.agents.update_one(
                        {"_id": self.doc["_id"]},
                        {"$set": {"status": False}}
                    )

                except pymongo.errors.PyMongoError:
                    print("mongo error")


class Hold():
    def __init__(self, docs):
        self.docs = docs
        self.events = {}

# запускает треды для всех агентов
    def start(self):
        for doc in self.docs:
            e = Event()
            self.events[doc['_id']] = e
            th = Thr(e, doc)
            th.start()

# запускает тред для нового агента
    def start_one(self, doc):
        self.docs.append(doc)
        db.agents.insert_one(doc)
        e = Event()
        self.events[doc['id']] = e
        th = Thr(e, doc)
        th.start()

    def stop(self):
        for k, e in self.events.items():
            #chto esli set setted event?
            e.set()

    def stop_one(self, x):
        e = self.events[x]
        e.set()

    def rm(self):
        for k, e in self.events.items():
            e.set()
        for d in self.docs:
            self.docs.remove(d)
        db.agents.drop()

    def rm_one(self, x):
        e = self.events[x]
        e.set()
        for d in self.docs:
            if d['_id'] == x:
                self.docs.remove(d)
                db.agents.delete_one({'_id': x})

    def update(self, x, doc):
        self.stop_one(x)
        self.start_one(doc)
        db.agents.update_one(
            {'_id': x},
            {'$set': {
                'name': doc['name'],
                'http': doc['http'],
                'period': doc['period']
            }}
        )


def code():
    db.edited.drop()
    db.edited.insert_one({'add': [], 'upd': {}, 'del': []})

    if "agents" not in db.collection_names():
        print('not found')

        with open('conf.json') as data:
            agents = (json.load(data))['agents']
            for agent in agents:
                db.agents.insert_one(agent)

    x = db.agents.find()
    h = Hold(x)

    try:
        h.start()

    except:
        h.stop()

    while True:

        edited = db.edited.find_one()

        for agent in edited['add']:
            h.start_one(agent)


        for idx, agent in edited['upd'].items():
            h.update(idx, agent)

        for idx in edited['del']:
            #добавить удаление всех, если совпадает число айди и агентов
            h.rm_one(idx)
        sleep(10)


class daemon2(daemon):
    def run(self):
        while True:
            try:
               code()
            except:
                pass
            else:
                break

if __name__ == "__main__":
    dae = daemon2('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            dae.start()
        elif 'stop' == sys.argv[1]:
            dae.stop()
        elif 'restart' == sys.argv[1]:
            dae.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)


 #   code()
