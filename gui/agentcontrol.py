import os
from tkinter import *
from tkinter.messagebox import *
from common import MyLabel, CommonFrame, ThemedButton
from web import Web


class AgentsControl(CommonFrame):

    checked_row = 0

    class Raw(Radiobutton):
        def __init__(self, parent, index, **kw):
            Radiobutton.__init__(self, parent, **kw)
            self.entryArray = []
            self.index = index
            self.empty = False

        def set_empty(self, state):
            self.empty = state

        def is_empty(self):
            return self.empty

        def enable(self):
            for ent in self.entryArray:
                ent.config(state=NORMAL)

        def disable(self):
            for ent in self.entryArray:
                ent.config(state="readonly")

        def append(self, item):
            self.entryArray.append(item)

        def current_state(self):
            for ent in self.entryArray:
                ent.insert_current()

        def focus_on_first_entry(self):
            self.entryArray[0].focus()

        def get_array(self):
            return self.entryArray

    class MyEntry(Entry):
        def __init__(self, parent, **kw):
            Entry.__init__(self, parent, **kw)

            self.current_state = ""

        def get_current(self):
            return self.current_state

        def insert_current(self):
            self.delete(0, END)
            self.insert(0, self.current_state)

        def insert(self, index, string):
            self.current_state = string
            Entry.insert(self, index, string)

        def change_state(self, state):
            self.current_state = state

    def __init__(self, parent, **kw):

        CommonFrame.__init__(self, parent, **kw)

        self.buttonText = ["+", "-", "M"]
        self.handlers = [self.add, self.delete, self.modify]
        self.labelText = ["name", "http", "period"]

        self.rawArray = []

        self.web = Web()

        self.agent = self.web.create_agent()
        self.amountOfAgents = len(self.agent.agents) + 1

        self.current_row = 0

    def pack(self, **kw):

        Frame.pack(self, **kw)
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.bottomFrame.pack(side=BOTTOM, expand=YES, fill=BOTH)

        self.bottomFrame.columnconfigure(0, weight=1)

        for (buttonName, labelName, i, handler) in zip(self.buttonText, self.labelText, range(1, 4), self.handlers):
            ThemedButton(self.topFrame, text=buttonName, command=handler).pack(side=LEFT)
            MyLabel(self.bottomFrame, text=labelName).grid(row=0, column=i, sticky=EW)
            self.bottomFrame.columnconfigure(i, weight=1)

        ThemedButton(self.topFrame, text="R", command=self.refresh).pack(side=LEFT)

        self.current_row += 1

        for i in range(1, self.amountOfAgents):
            self.current_row += 1

            raw = self.Raw(self.bottomFrame, i, value=i, command=lambda index=i: self.radioButtonCallback(index))

            if i == 1:
                raw.select()

            raw.grid(row=i, column=0)

            self.rawArray.append(raw)

            for j in range(1, 4):
                ent = self.MyEntry(self.bottomFrame, width=15)
                ent.insert(0, self.agent.info[i-1][j-1])

                raw.append(ent)
                ent.grid(row=i, column=j, sticky=EW)

            if i != 1:
                raw.disable()

        self.add_empty_raw()

    def add_empty_raw(self):
        # Пустая строка для добавления агента

        raw = self.Raw(self.bottomFrame, self.current_row, value=self.current_row, command=lambda index=self.current_row: self.radioButtonCallback(index))
        raw.set_empty(True)
        raw.grid(row=self.current_row, column=0)

        self.rawArray.append(raw)

        for j in range(1, 4):
            ent = self.MyEntry(self.bottomFrame, width=15)

            raw.append(ent)
            ent.grid(row=self.current_row, column=j, sticky=EW)

        self.current_row += 1

    def radioButtonCallback(self, index):
        if not self.rawArray[self.checked_row].is_empty():
            self.rawArray[self.checked_row].current_state()
            self.rawArray[self.checked_row].disable()

        self.checked_row = index - 1
        self.rawArray[self.checked_row].focus_on_first_entry()
        self.rawArray[self.checked_row].enable()
        print("You've just clicked on %d" % index)

    def validate(self, name, url, period, index):
        err = False
        for (item, arr, errmsg) in zip((name, url), (self.agent.agents, self.agent.urls),
                                        ("Данное имя уже используется", "Данный адрес уже используется")):
            if not self.validation(item, arr, index):
                showerror("error!", errmsg)
                err = True

        if not self.check_url(url):
            showerror("error!", "Данный адрес некорректен")
            err = True

        if not self.check_period(period):
            showerror("error!", "Данный период некорректен")
            err = True
        return err

    def add(self):

        if "" in [self.rawArray[self.current_row-2].get_array()[i].get() for i in range(3)]:
            showerror("error!", "Заполните все поля")
            return

        name = self.rawArray[self.current_row - 2].get_array()[0].get()
        url = self.rawArray[self.current_row - 2].get_array()[1].get()
        period = self.rawArray[self.current_row - 2].get_array()[2].get()

        if url[-1] != "/":
            url += "/"

        if not self.validate(name, url, period, self.current_row):
            showinfo("info", "Агент добавлен")
            self.web.add_agent(name, url, float(period))

            self.rawArray[self.current_row - 2].get_array()[0].change_state(name)
            self.rawArray[self.current_row - 2].get_array()[1].change_state(url)
            self.rawArray[self.current_row - 2].get_array()[2].change_state(period)

            self.agent.agents.append(name)
            self.agent.urls.append(url)
            self.agent.periods.append(float(period))

            self.rawArray[self.current_row - 2].set_empty(False)
            self.rawArray[self.current_row - 2].disable()
            self.add_empty_raw()

    def delete(self):
        # TODO сделать более быстрое удаление

        self.web.delete_agent(self.agent.ids[self.agent.agents[self.checked_row]])
        showinfo("info", "Агент удален")

    def modify(self):
        name = self.rawArray[self.checked_row].get_array()[0].get()
        url = self.rawArray[self.checked_row].get_array()[1].get()
        period = self.rawArray[self.checked_row].get_array()[2].get()

        if url[-1] != "/":
            url += "/"

        if not self.validate(name, url, period, self.checked_row):
            showinfo("info", "Агент модифицирован")
            self.conf.change_agent(self.checked_row, name, url, float(period))

            self.rawArray[self.checked_row].get_array()[0].change_state(name)
            self.rawArray[self.checked_row].get_array()[1].change_state(url)
            self.rawArray[self.checked_row].get_array()[2].change_state(period)

            self.agent.agents[self.checked_row] = name
            self.agent.urls[self.checked_row] = url
            self.agent.periods[self.checked_row] = float(period)

    def refresh(self):
        self.canvas.delete(ALL)
        self.canvas.destroy()
        self.__init__(self.parent)
        self.pack(expand=YES, fill=BOTH)

    def validation(self, name, array, index):
        for (item, i) in zip(array, range(len(array))):
            if name == item and i != index:
                return False
        return True

    @staticmethod
    def update_time(filename):
        return os.path.getmtime(filename)

    def check_period(self, period):
        try:
            float(period)
            return True
        except ValueError:
            return False

    def check_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not re.match(regex, url) or url[-1] != '/':
            return False

        return True

