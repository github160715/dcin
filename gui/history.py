from common import MyLabel, CommonFrame, ThemedButton
from tkinter import *
from web import Web
from tkinter.messagebox import *
import requests


class SmartEntry(Entry):
    def __init__(self, parent, text, first=True, **kw):
        self.first = first

        if first:
            Entry.__init__(self, parent, font=("Helvetica", 10, "italic"), width=30, fg="light grey")
        else:
            Entry.__init__(self, parent, width=30)

        self.insert(0, text)

        self.bind('<FocusIn>', self.focus_in)

    def focus_in(self, event):
        if self.first:
            self.delete(0, END)
            self.first = False
            self.config(font=("Helvetica", 10), fg="black", width=30)


class History(CommonFrame):
    def __init__(self, parent, start, end, first, **kw):
        CommonFrame.__init__(self, parent, **kw)

        self.parent = parent

        self.current_row = 0

        self.headers = ["name", "date", "cpu", "memory"]

        self.web = Web()

        self.btn = ThemedButton(self.topFrame, text="OK", command=self.accept)

        self.start = SmartEntry(self.topFrame, start, first)

        self.end = SmartEntry(self.topFrame, end, first)

        self.amountOfEntries = 0

    def pack(self, **kw):
        Frame.pack(self, **kw)

        try:
            self.info = self.web.get_info(self.start.get(), self.end.get())

        except requests.RequestException:
            showerror("error!", "Не могу соединиться с веб службой")
            self.info = []

        self.amountOfEntries = len(self.info)

        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, expand=YES, fill=BOTH)

        self.bottomFrame.columnconfigure(0, weight=1)

        self.start.pack(side=LEFT)
        self.end.pack(side=LEFT)

        self.btn.pack(side=LEFT)
        self.btn.focus()

        for (i, text) in zip(range(4), self.headers):
            MyLabel(self.bottomFrame, text=text).grid(row=0, column=i, sticky=EW)
            self.bottomFrame.columnconfigure(i, weight=1)

        self.current_row += 1

        for i in range(0, self.amountOfEntries):
            for (j, item) in zip(range(0, 4), (self.info[i]['agent'], self.info[i]['time'], self.info[i]['cpu'], self.info[i]['used'])):
                ent = Entry(self.bottomFrame, width=20)
                ent.insert(0, item)
                ent.config(state="readonly")

                ent.grid(row=i + 1, column=j, sticky=EW)

            self.current_row += 1

    def accept(self):
        start = self.start.get()
        end = self.end.get()

        if not start or not end:
            showerror("error!", "Заполните все поля")
            return
        if not self.web.date_validator(start) or not self.web.date_validator(end):
            showerror("error!", "Используйте следующий формат даты\n2015-07-27T07:27:10.658Z")
            return

        self.canvas.delete(ALL)
        self.canvas.destroy()
        self.__init__(self.parent, start, end, False)
        self.pack(expand=YES, fill=BOTH)
