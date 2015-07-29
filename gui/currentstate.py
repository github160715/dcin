from common import MyCanvas, MyLabel, CommonFrame, ThemedButton
from tkinter import *
from web import Web
from tkinter.messagebox import *
import requests


class ColoredEntry(Entry):
    def __init__(self, parent, **kw):
        Entry.__init__(self, parent, **kw)


class CurrentState(CommonFrame):
    def __init__(self, parent, **kw):
        CommonFrame.__init__(self, parent, **kw)

        self.parent = parent

        self.current_row = 0

        self.headers = ["name", "state", "cpu", "memory"]

        self.web = Web()

        try:
            self.agents, self.statuses, self.last_info = self.web.get_current()

        except requests.RequestException:
            showerror("error!", "Не могу соединиться с веб службой")
            self.agents = []

        self.amountOfAgents = len(self.agents)

    def pack(self, **kw):
        Frame.pack(self, **kw)

        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, expand=YES, fill=BOTH)

        self.bottomFrame.columnconfigure(0, weight=1)

        ThemedButton(self.topFrame, text="R", command=self.refresh).pack(side=LEFT)

        for (i, text) in zip(range(4), self.headers):
            MyLabel(self.bottomFrame, text=text).grid(row=0, column=i, sticky=EW)
            self.bottomFrame.columnconfigure(i, weight=1)

        self.current_row += 1

        for i in range(0, self.amountOfAgents):
            for (j, item) in zip(range(0, 4), (self.agents[i], self.statuses[self.agents[i]], self.last_info[self.agents[i]]["cpu"], self.last_info[self.agents[i]]["used"])):
                if j == 1 and item == "on":
                    bg = "green"
                elif j == 1:
                    bg = "red"
                else:
                    bg = "light grey"
                ent = ColoredEntry(self.bottomFrame, width=15, readonlybackground=bg)
                ent.insert(0, item)
                ent.config(state="readonly")

                ent.grid(row=i + 1, column=j, sticky=EW)

            self.current_row += 1

    def refresh(self):
        self.canvas.delete(ALL)
        self.canvas.destroy()
        self.__init__(self.parent)
        self.pack(expand=YES, fill=BOTH)