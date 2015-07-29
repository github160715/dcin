
import requests
import json
import time

def writing(url, file):
    r1 = requests.get(url)
    json.dump(r1.json(), file)
    file.write("\n")
def serv(js, errf):
    for agent in js :
        x = js[agent]
        cpu = 'http://localhost:'+x+'/vals/cpu'
        memory = 'http://localhost:'+x+'/vals/memory'
        file = open('file'+x, 'a+')
        try:
            writing(cpu, file)
            writing(memory, file)
        except:
            json.dump({x: time.localtime()}, errf)
            errf.write("\n")
        file.close()
#main
conf_file = open('config.json', 'r')
config = json.load(conf_file)
conf_file.close()
err_file = open(config['errors'], 'a+')
js = config['agents']
p = int(config['period'])
while True:
    while True:
        try:
            serv(js, err_file)
        except:
            pass
        else:
            break
    time.sleep(p)
err_file.close()