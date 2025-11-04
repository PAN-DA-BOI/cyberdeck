import tkinter as tk
import os
from tkinter import messagebox
from utils import clear_page, update_file_list
from globals import *

def file_viewer(main, homepage, callback, mode="open"):
    """
    mode: "open" or "save"
    callback: function to call with the selected file path
    """
    # Clear the current page
    for widget in main.winfo_children():
        widget.destroy()

    # --- State ---
    current_path = os.getcwd()
    selected_index = 0
    file_list = []
    filename_entry = None

    # --- Widgets ---
    frame = tk.Frame(
        master=main,
        bg="#000000",
        highlightbackground="#00FF00",
        highlightthickness=2
    )
    frame.place(x=60, y=20, width=800, height=480)

    back_button = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="Back"
    )
    back_button.place(x=880, y=180, width=120, height=80)

    select_button = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="Select" if mode == "open" else "Save"
    )
    select_button.place(x=880, y=380, width=120, height=80)

    if mode == "save":
        filename_frame = tk.Frame(
            master=main,
            bg="#000000",
            highlightbackground="#00FF00",
            highlightthickness=2
        )
        filename_frame.place(x=60, y=500, width=800, height=40)

        filename_label = tk.Label(
            filename_frame,
            text="Filename:",
            bg="#000000",
            fg="#00FF00",
            font=("Arial", 10)
        )
        filename_label.place(relx=0, rely=0, relwidth=0.2, height=40)

        filename_entry = tk.Entry(
            filename_frame,
            bg="#000000",
            fg="#00FF00",
            highlightbackground="#00FF00",
            highlightthickness=1
        )
        filename_entry.place(relx=0.2, rely=0, relwidth=0.7, height=40)
        filename_entry.insert(0, "untitled.txt")

    # --- Functions ---
    def update_file_list():
        nonlocal file_list
        try:
            file_list = [".."] + [f for f in os.listdir(current_path)]
        except Exception as e:
            file_list = [f"Error: {e}"]

    def draw_file_list():
        for widget in frame.winfo_children():
            widget.destroy()
        for i, item in enumerate(file_list):
            bg = "#00FF00" if i == selected_index else "#000000"
            name_label = tk.Label(
                frame,
                text=item,
                bg=bg,
                fg="#00FF00",
                font=("Arial", 10),
                anchor="w"
            )
            name_label.place(relx=0, rely=i/10, relwidth=0.7, height=40)

            if item == "..":
                type_text = "Parent Directory"
            elif os.path.isdir(os.path.join(current_path, item)):
                type_text = "Folder"
            else:
                ext = os.path.splitext(item)[1]
                type_text = ext[1:] if ext else "File"
            type_label = tk.Label(
                frame,
                text=type_text,
                bg=bg,
                fg="#FF00FF",
                font=("Arial", 10),
                anchor="e"
            )
            type_label.place(relx=0.7, rely=i/10, relwidth=0.3, height=40)

    def on_key_file(event):
        nonlocal selected_index, current_path
        if event.keysym == "Right" and selected_index < len(file_list) - 1:
            selected_index += 1
            draw_file_list()
        elif event.keysym == "Left" and selected_index > 0:
            selected_index -= 1
            draw_file_list()
        elif event.keysym == "Return":
            selected_item = file_list[selected_index]
            if selected_item == "..":
                current_path = os.path.dirname(current_path)
            elif os.path.isdir(os.path.join(current_path, selected_item)):
                current_path = os.path.join(current_path, selected_item)
            else:
                if mode == "open":
                    callback(os.path.join(current_path, selected_item))
                    return
                elif mode == "save":
                    filename = filename_entry.get().strip()
                    if filename:
                        callback(os.path.join(current_path, filename))
                        return
            selected_index = 0
            update_file_list()
            draw_file_list()
        elif event.keysym == "Escape":
            homepage(main)

    def on_key_button(event):
        if event.keysym == "Escape":
            homepage(main)

    # --- Bindings ---
    frame.bind("<Left>", on_key_file)
    frame.bind("<Right>", on_key_file)
    frame.bind("<Return>", on_key_file)
    frame.bind("<Escape>", lambda e: homepage(main))
    back_button.bind("<Return>", lambda e: homepage(main))
    back_button.bind("<Escape>", lambda e: homepage(main))
    select_button.bind("<Return>", lambda e: on_key_file(tk.Event(keysym="Return")))
    select_button.bind("<Escape>", lambda e: homepage(main))
    if mode == "save":
        filename_entry.bind("<Escape>", lambda e: homepage(main))
        filename_entry.bind("<Return>", lambda e: on_key_file(tk.Event(keysym="Return")))

    # --- Initialize ---
    update_file_list()
    draw_file_list()
    frame.focus_set()
