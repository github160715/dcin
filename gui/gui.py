#!/usr/bin/env python3

from tkinter import ttk
from tkinter import *
from agentcontrol import AgentsControl
from currentstate import CurrentState
from history import History
import json
import os


def get_conf():
    with open("conf.json") as conf_file:
        return json.load(conf_file)


class Gui(ttk.Notebook):

    def __init__(self, parent):
        ttk.Notebook.__init__(self, parent)

        agents = Frame(self)
        AgentsControl(agents).pack(expand=YES, fill=BOTH)

        state = Frame(self)
        CurrentState(state).pack(expand=YES, fill=BOTH)

        history = Frame(self)
        History(history, "2015-07-27T07:27:10.658Z", "2015-07-27T07:28:10.658Z", True).pack(expand=YES, fill=BOTH)

        self.add(agents, text='Управление агентами')
        self.add(state, text='Текущее состояние')
        self.add(history, text='История')

        self.pack(expand=YES, fill=BOTH)

if __name__ == '__main__':

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    root = Tk()
    root.title("Monitoring")

    conf = get_conf()

    root.geometry(str(conf["width"])+"x"+str(conf["height"]))
    Gui(root)
    root.mainloop()
