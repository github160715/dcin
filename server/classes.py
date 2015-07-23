import requests
import json
import datetime
import pymongo
from pymongo import MongoClient
from datetime import datetime


class Agent:
    def __init__(self, name, address, err):

        self.name = name
        self.address = address
        self.err = err
        self.db = MongoClient().test

        try:
            with open(self.name + '.json', 'w') as f:
                    json.dump([], f)

        except OSError:
            print("Can't create " + self.name + '.json')

    def get_data(self):
        json_obj = {}
        try:
            r = requests.get(self.address + "vals/cpu")
            cpu_json = json.loads(r.text)

            r = requests.get(self.address + "vals/memory")
            memory_json = json.loads(r.text)

            try:
                json_obj = self.create_json(cpu_json, memory_json)
                self.append_data(json_obj)
                self.mongo_insert(json_obj, True)

            except KeyError:
                print(self.name + " can't connect to db")
                self.mongo_insert(json_obj, False)

        except requests.RequestException:
            try:
                self.mongo_insert(json_obj, False)
                with open(self.err, "a") as f:
                    f.write(datetime.now().strftime("%y/%m/%d %H:%M:%S")
 + "  " + self.name + " is unavailable" + "\n")
                self.append_data("error")

            except OSError:
                print("Can't open " + self.err)

    def append_data(self, data):
        try:
                with open(self.name + '.json') as f:
                    data_json = json.load(f)
                data_json.append(data)

                with open(self.name + '.json', 'w') as f:
                    json.dump(data_json, f)

        except OSError: # parent of IOError, OSError *and* WindowsError where available
            print("Can't open " + self.name + '.json')

    def create_json(self, cpu, memory):
        return {str(cpu["time"]): {"cpu": cpu["cpu"], "total": memory["total"], "used": memory["used"]}}

    def delete_agent(self, i):
        try:
            with open('conf.json') as f:
                data_json = json.load(f)

            data_json["agents"].pop(i)

            with open('conf.json', 'w') as f:
                json.dump(data_json, f)

            try:
                self.db.agents.delete_one({"name": self.name})
                self.db.states.delete_many({"agent": self.name})

            except pymongo.errors.PyMongoError:
                print("error")

        except OSError: # parent of IOError, OSError *and* WindowsError where available
            print("Can't open " + self.name + '.json')

    def mongo_insert(self, data, on):

        if on:
            time = list(data.keys())[0]
            last = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
            status = "on"

            try:
                self.db.states.insert_one({
                    "agent": self.name,
                    "time": last,
                    "cpu": data[time]["cpu"],
                    "total": data[time]["total"],
                    "used": data[time]["used"]
                })
            except pymongo.errors.PyMongoError:
                print("error")
        else:
            last = None
            status = "off"

        try:
            if self.db.agents.find({"name": self.name}).limit(1).count() > 0:
                if on:
                    self.db.agents.update_one(
                        {"name": self.name},
                        {"$set": {
                            "status": status,
                            "last": last
                                 }
                        }
                    )
                else:
                    self.db.agents.update_one(
                        {"name": self.name},
                        {"$set": {
                            "status": status,
                        }
                        }
                    )

            else:

                self.db.agents.insert_one({
                    "name": self.name,
                    "status": status,
                    "last": last
                })

        except pymongo.errors.PyMongoError:
            print("error")



