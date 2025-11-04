import tkinter as tk
from Applications.notepad import notepad
from Applications.comms import comms
from Applications.browser import browser_search
from Applications.camera_sync import camera_sync
from utils import clear_page
from globals import *

def homepage(main):
    clear_page(main)
    global current_widgets

    # --- Buttons ---
    button = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="Notepad"
    )
    button.place(x=20, y=20, width=980, height=120)
    label = tk.Label(
        button,
        text="Notepad",
        bg="#000000",
        fg="#00FF00",
        font=("Arial", 12)
    )
    label.place(relx=0.5, rely=0.5, anchor="center")

    button1 = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="COMMS"
    )
    button1.place(x=20, y=160, width=980, height=120)
    label1 = tk.Label(
        button1,
        text="COMMS",
        bg="#000000",
        fg="#00FF00",
        font=("Arial", 12)
    )
    label1.place(relx=0.5, rely=0.5, anchor="center")

    browser_button = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="Browser"
    )
    browser_button.place(x=20, y=300, width=980, height=120)
    label2 = tk.Label(
        browser_button,
        text="Browser",
        bg="#000000",
        fg="#00FF00",
        font=("Arial", 12)
    )
    label2.place(relx=0.5, rely=0.5, anchor="center")

    camera_button = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="Camera Sync"
    )
    camera_button.place(x=20, y=440, width=980, height=120)

    # --- Widget List ---
    current_widgets = [button, button1, browser_button, camera_button]
    current_widgets[0].focus_set()

    # --- Button Commands ---
    button.config(command=lambda: notepad(main, homepage))
    button.bind("<Return>", lambda e: notepad(main, homepage))
    button1.config(command=lambda: comms(main, homepage))
    button1.bind("<Return>", lambda e: comms(main, homepage))
    browser_button.config(command=lambda: browser_search(main, homepage))
    browser_button.bind("<Return>", lambda e: browser_search(main, homepage))
    camera_button.config(command=lambda: camera_sync(main, homepage))
    camera_button.bind("<Return>", lambda e: camera_sync(main, homepage))



