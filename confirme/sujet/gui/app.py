import tkinter as tk
import customtkinter as ctk
from .sidebar import Sidebar
from .statusbar import Statusbar
from .mainview import Mainview
from .dijactor import Dijactor


class App(ctk.CTk):
    def __init__(self, img):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        super().__init__()
        self.resizable(False, False)
        self.title("Don't worry be heap.py!")
        self.iconphoto = tk.PhotoImage(file="data/bruE.png")
        self.wm_iconphoto(False, self.iconphoto)
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        self.config(menu="")
        self.bind("<Control-q>", lambda event: self.destroy())
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.sidebar = Sidebar(self)
        self.status = Statusbar(self)
        h = img.size[1]
        assert h <= 800
        sc = 2 * (((800 // h) - 1) // 2) + 1
        self.canvas = Mainview(self, img, sc)
        self.reactor = Dijactor(self, img, sc)
        self.bind("<<RefreshIMG>>", self.canvas.refreshimg)
        self.status.hidebar()

    def reload(self):
        self.reactor.reload()
        self.canvas.reset()

    def changeprio(self, choice):
        self.reactor.setprio(choice)
        self.canvas.reset()
