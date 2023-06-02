import tkinter as tk
from enum import Enum
from PIL import Image, ImageTk


State = Enum("State", "START DIJKSTRA END".split())

cursors = {State.START: "tcross", State.DIJKSTRA: "plus", State.END: "circle"}


class Mainview(tk.Canvas):
    sc = 11
    w, h = 64, 64
    state = State.START
    source = None
    fresh = True

    def __init__(self, master, img, sc, **kwargs):
        self.w, self.h = img.size
        self.sc = sc
        self.img = img.resize((self.w * self.sc, self.h * self.sc), Image.BOX)
        super().__init__(
            master=master,
            width=self.img.size[0],
            height=self.img.size[1],
            border=0,
            highlightthickness=0,
            **kwargs,
        )
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvasimage = self.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.bind("<Motion>", self.moved)
        self.bind("<Button-1>", self.clicked)
        self.bind("<Button-2>", self.undo)
        self.bind("<Button-3>", self.undo)
        self.grid(row=0, column=0, sticky=None)
        self.upcursor()

    def reset(self):
        self.state = State.START
        self.upcursor()

    def upcursor(self):
        self.config(cursor=cursors[self.state])

    def inprogress(self):
        return self.state != State.END

    def moved(self, event):
        x = int(event.x / self.sc)
        y = int(event.y / self.sc)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.master.status.stmsg.set(f"{x}, {y}")
            if self.state is not State.END:
                self.master.reactor.setdest((x, y))

    def refreshimg(self, event):
        self.photo = ImageTk.PhotoImage(self.img)
        self.itemconfig(self.canvasimage, image=self.photo)
        self.fresh = True

    def undo(self, event):
        if self.state == State.END:
            self.state = State.DIJKSTRA
            self.upcursor()
        self.master.reactor.undo()
        news = self.master.reactor.lastpoint()
        if news is not None:
            self.master.reactor.launch(*news)
        else:
            self.state = State.START
            self.upcursor()

    def clicked(self, event):
        x = int(event.x / self.sc)
        y = int(event.y / self.sc)
        if 0 < x < self.w - 1 and 0 < y < self.h - 1:
            if self.state == State.START:
                self.state = State.DIJKSTRA
                self.upcursor()
                self.master.reactor.launch(x, y)
            elif self.state == State.DIJKSTRA:
                if self.master.reactor.addpoint(x, y):
                    if self.master.reactor.closed():
                        self.state = State.END
                        self.upcursor()
                        self.master.reactor.tadam()
                    else:
                        self.master.reactor.reset()
                        self.master.reactor.launch(x, y)
