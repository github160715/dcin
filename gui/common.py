from tkinter import *


class CommonFrame(Frame):
    def __init__(self, parent, **kw):

        Frame.__init__(self, parent, **kw)

        self.canvas = MyCanvas(self, borderwidth=0, background="#FFFFFF")
        self.frame = Frame(self.canvas, background="#FFFFFF")

        self.parent = parent

        self.topFrame = Frame(self.frame)
        self.bottomFrame = Frame(self.frame)

        self.vsb = Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.create_window((0, 0), window=self.frame, width=400, anchor="nw", tag="window")


class MyCanvas(Canvas):
    def __init__(self, parent, **kw):
        Canvas.__init__(self, parent, **kw)

        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        self.configure(scrollregion=self.bbox("all"))

        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height

        self.width = event.width
        self.height = event.height

        # resize the canvas
        self.config(width=self.width, height=self.height)

        # rescale all the objects tagged with the "all" tag
        self.scale(ALL, 0, 0, wscale, hscale)


class MyLabel(Label):
    def __init__(self, parent, text):

        Label.__init__(self, parent, text=text, relief=RIDGE, width=25, height=2)


class ThemedButton(Button):
    def __init__(self, parent, text, **kw):

        Button.__init__(self, parent, text=text, height=1, width=3, **kw)
