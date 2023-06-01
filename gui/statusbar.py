import customtkinter as ctk
from tktooltip import ToolTip


class Statusbar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.grid(row=1, column=0, sticky="nsew")

        self.master.vispan = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(
            self,
            text="Debug",
            command=self.switch_event,
            variable=self.master.vispan,
            onvalue="on",
            offvalue="off",
            progress_color="#F00",
        )
        self.switch.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")
        self.master.bind("<Tab>", self.switch.toggle)
        self.master.bind("<<ProgressBar>>", self.setbar)
        self.stmsg = ctk.StringVar(self, "")
        self.stlabel = ctk.CTkLabel(master=self, textvariable=self.stmsg, width=64)
        self.stlabel.grid(row=0, column=2, padx=4, pady=4, stick="nse")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.progressbar = ctk.CTkProgressBar(
            self, orientation="horizontal", progress_color="#AA0", corner_radius=1
        )
        self.progressbar.grid(row=0, column=1, padx=4, pady=4, stick="we")
        self.barval = 0
        self.fresh = True
        self.progressbar.set(0)
        ToolTip(self.progressbar, msg="progression de Dijkstra")

    def setbar(self, event):
        self.fresh = True
        if self.barval is None:
            self.hidebar()
        else:
            self.progressbar.set(self.barval)

    def showbar(self):
        self.progressbar.grid()
        self.progressbar.update_idletasks()

    def hidebar(self):
        self.progressbar.grid_remove()

    def switch_event(self):
        if self.master.vispan.get() == "on":
            self.master.sidebar.update_switches()
            self.master.sidebar.show()
        else:
            self.master.reactor.showF = False
            self.master.reactor.showP = False
            self.master.sidebar.hide()
        if self.master.canvas.inprogress():
            self.master.reactor.updatefromdec(None)
