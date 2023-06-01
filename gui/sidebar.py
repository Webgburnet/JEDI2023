import customtkinter as ctk
import prios


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.grid_rowconfigure((0, 1, 2, 3, 5), weight=0)
        self.grid_rowconfigure(6, weight=1)

        self.debug = ctk.CTkLabel(
            self,
            text="File de priorité",
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
        )
        self.debug.grid(row=0, column=0, padx=8, pady=4, stick="we")
        self.priovar = ctk.StringVar(value=prios.default)
        self.priomenu = ctk.CTkOptionMenu(
            self,
            values=prios.choices,
            variable=self.priovar,
            command=self.master.changeprio,
        )
        self.priomenu.grid(row=1, column=0, padx=8, pady=8, stick="we")
        self.master.visF = ctk.StringVar(value="on")
        self.switchF = ctk.CTkSwitch(
            self,
            text="Visualiser la file",
            command=self.switch_eventF,
            variable=self.master.visF,
            onvalue="on",
            offvalue="off",
            progress_color="#F00",
        )
        self.switchF.grid(row=2, column=0, padx=8, pady=8, stick="we")
        self.master.visP = ctk.StringVar(value="on")
        self.switchP = ctk.CTkSwitch(
            self,
            text="Visualiser les chemins",
            command=self.switch_eventP,
            variable=self.master.visP,
            onvalue="on",
            offvalue="off",
            progress_color="#F00",
        )
        self.switchP.grid(row=3, column=0, padx=8, pady=8, stick="we")
        self.labvit = ctk.CTkLabel(
            self,
            text="Vitesse d'affichage :",
            anchor="w",
        )
        self.labvit.grid(row=4, column=0, padx=8, pady=4, stick="we")
        self.vitesse = ctk.CTkSlider(
            self, from_=0, to=16, number_of_steps=16, command=self.set_speed
        )
        self.vitesse.set(16)
        self.vitesse.grid(row=5, column=0, padx=8, pady=8, stick="we")
        self.button = ctk.CTkButton(
            self,
            text="Recharger",
            command=self.master.reload,
            fg_color="#F00",
            hover_color="#900",
        )
        self.button.grid(row=6, column=0, padx=8, pady=8, stick="swe")
        self.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.grid_remove()

    def show(self):
        self.grid()
        self.update_idletasks()

    def hide(self):
        self.grid_remove()

    def set_speed(self, value):
        v = 2 ** int(value) if value < 16 else None
        self.master.reactor.setspeed(v)

    def switch_eventF(self):
        self.master.reactor.showF = self.master.visF.get() == "on"
        self.master.reactor.updatefromdec(None)

    def switch_eventP(self):
        self.master.reactor.showP = self.master.visP.get() == "on"
        self.master.reactor.updatefromdec(None)

    def update_switches(self):
        self.master.reactor.showF = self.master.visF.get() == "on"
        self.master.reactor.showP = self.master.visP.get() == "on"
