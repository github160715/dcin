import json
from classes import Agent


def create_agents(conf):
    list_of_agents = []
    for key in conf["agents"]:
        list_of_agents.append(Agent(key, conf["agents"][key], conf["error_file"]))
    return list_of_agents

def get_conf():
    with open("conf.json") as conf_file:
        return json.load(conf_file)

if __name__ == "__main__" :
    agents = create_agents(get_conf())
    for agent in agents:
        agent.get_data()
    # a = Agent("agent1", "http://localhost:8010/", "error_file")
    # a.get_data()
    # a.get_data()
    # a.get_data()
    # for key in conf:
    #     print(key, end=" ")
    #     get_data(conf[key])
    #print(conf["first address"])

# requests = requests.get("http://localhost:3000/test/datetime_now")
# print(r.status_code)
# print(r.text)
# obj = r.json()
#
# for key in obj:
#     print(key + ":" + obj[key])
#
# r = requests.get("http://localhost:3000/test/datetime_now", params={"param1" : "value1", "param2" : 666})
# print(r.json())
#
# r = requests.post("http://localhost:3000/test/datetime_now", data={"param1" : "value1", "param2" : 666})
# print(r.json())
#
# f = open("file.txt", "w")
# f.write("line1\n")
# f.close()
#
# f = open("file.txt", "r")
# print(f.read())
# r.close()
