import requests
import json
import datetime


class Agent:
    def __init__(self, name, address, err):
        self.name = name
        self.address = address
        self.err = err
        self.counter = 0

    def get_data(self):
        self.write_data(self.name + ".txt", "request number %d" % self.counter)
        self.counter += 1
        try:
            r = requests.get(self.address + "cpu")
            data = json.loads(r.text)
            text = str(data["current_time"]) + " : " + str(data["cpu"])
            self.write_data(self.name + ".txt", text)

            r = requests.get(self.address + "memory")
            data = json.loads(r.text)
            text = str(data["current_time"]) + " : " + str(data["memory"])
            self.write_data(self.name + ".txt", text)

        except:
            self.write_data(self.name + ".txt", "Error, check " + self.err + " to see more details")
            self.write_data(self.err + ".txt", datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S")
 + "  " + self.name + " is unavailable")

        finally:
            self.write_data(self.name + ".txt", "")

    def write_data(self, filename,  text):
        try:
            with open(filename, "a") as f:
                f.write(text + "\n")
        except:
            print("Can't open " + self.name + ".txt")
