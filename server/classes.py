import requests
import json
import datetime


class Agent:
    def __init__(self, name, address, err):
        self.name = name
        self.address = address
        self.err = err

        try:
            with open(self.name + '.json', 'w') as f:
                    json.dump([], f)

        except OSError:
            print("Can't create " + self.name + '.json')

    def get_data(self):
        try:
            r = requests.get(self.address + "cpu")
            cpu_json = json.loads(r.text)

            r = requests.get(self.address + "memory")
            memory_json = json.loads(r.text)

            try:
                self.append_data(self.create_json(cpu_json, memory_json))

            except KeyError:
                print(self.name + " can't connect to db")

        except requests.RequestException:
            try:
                with open(self.err, "a") as f:
                    f.write(datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
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
        return {str(cpu["current_time"]) : { "cpu" : cpu["cpu"], "memory" : memory["memory"]}}



