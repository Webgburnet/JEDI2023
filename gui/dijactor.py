import tkinter as tk
import traceback
import reloader
from time import time
import sys
from .traceback_gui import show_traceback
from imgraph import GDelta
from threading import Thread
from wrap import classwrap
from debug import decorator
from tracer import Tracer

reloader.enable()
import prios
import dijkstra


class DijRunner(Thread):
    def __init__(self, master):
        self.master = master
        super().__init__()

    def run(self):
        t0 = time()
        self.master.computing = True
        try:
            self.master.dij(self.master.G, self.master.source)
            self.master.updatefromdec(None)
        except Exception as e:
            if type(e) is not STOPCOMPUTING:
                self.master.trace = sys.exc_info()[1]
                self.master.master.event_generate("<<BUGREPORT>>", when="tail")
        self.master.computing = False
        self.master.updateprogress(None)


class STOPCOMPUTING(Exception):
    pass


class Dijactor:
    def __init__(self, master, img, sc):
        self.master = master
        self.img = img
        self.sc = sc
        self.G = GDelta(img)
        self.size = len(self.G)
        self.stepsize = self.size // 8
        self.prio = prios.default
        self.computing = False
        self.runner = None
        self.dec = None
        self.speed = 1
        self.autospeed = True
        self.source = None
        self.dest = None
        self.trace = None
        self.showF = False
        self.showP = False
        self.fullreset()
        self.master.bind("<<BUGREPORT>>", self.bugreport)

    def setprio(self, prio):
        if prio != self.prio:
            self.prio = prio
            self.fullreset()

    def fullreset(self):
        self.segments = []
        self.reset()

    def setspeed(self, value):
        if value is None:
            self.autospeed = True
            self.speed = 1
        else:
            self.autospeed = False
            self.speed = value

    def reset(self):
        def spyinit(this):
            this.steps = 0

        def spy(this, attr, args, r):
            this.steps += 1
            if this.steps % self.stepsize == 0:
                self.updateprogress(this.steps / self.size)
            if this.steps % self.speed == 0:
                if not self.updatefromdec(r[0]) and self.autospeed:
                    self.speed *= 2
            if not self.computing:
                raise STOPCOMPUTING
            return r

        PafDict = classwrap(
            prios.get[self.prio], rets={"pop_smallest": spy}, init=spyinit
        )
        self.dij = dijkstra.Dijkstra(PafDict)
        self.computing = False
        self.runner = None
        self.dec = decorator(self.img, sc=self.sc)
        self.updateimg(self.dec.img)
        self.updateprogress(None, force=True)

    def updateimg(self, img):
        self.master.canvas.img = img
        if self.master.canvas.fresh:
            self.master.canvas.fresh = False
            self.master.event_generate("<<RefreshIMG>>", when="tail")
            return True
        return False

    def updatefromdec(self, last):
        if self.dec:
            return self.updateimg(
                self.dec(
                    self.dij.F,
                    self.dij.p,
                    self.source,
                    self.dest,
                    last,
                    self.segments,
                    self.showF,
                    self.showP,
                )
            )
        return False

    def updateprogress(self, value, force=False):
        self.master.status.barval = value
        if force or self.master.status.fresh:
            self.master.status.fresh = False
            self.master.event_generate("<<ProgressBar>>", when="tail")

    def launch(self, x, y):
        self.master.status.showbar()
        self.source = (x, y)
        if not self.segments:
            self.segments = [[(x, y)]]
        self.dest = (x, y)
        assert not self.computing
        self.runner = DijRunner(self)
        self.runner.start()

    def setdest(self, z):
        self.dest = z
        if not self.computing and self.dec is not None:
            self.updatefromdec(None)

    def addpoint(self, x, y):
        if self.dij:
            l = self.dij.shortest_path((x, y))
            if l:
                self.segments.append(l)
                return True
        return False

    def lastpoint(self):
        if self.segments:
            return self.segments[-1][-1]
        return None

    def closed(self):
        if self.segments:
            (x, y) = self.segments[0][0]
            (xx, yy) = self.segments[-1][-1]
            return abs(x - xx) <= 1 and abs(y - yy) <= 1
        return False

    def tadam(self):
        res = Tracer(self.img, compose=True, sc=self.sc)(self.segments)
        self.updateimg(res)

    def undo(self):
        if self.segments:
            del self.segments[-1]
        self.reset()

    def reload(self):
        try:
            reloader.reload(prios)
            reloader.reload(dijkstra)
            self.master.sidebar.priomenu.configure(values=prios.choices)
            self.fullreset()
            tk.messagebox.showerror("Ok", "C'est fait !")
        except:
            show_traceback()

    def bugreport(self, event):
        show_traceback(self.trace)
