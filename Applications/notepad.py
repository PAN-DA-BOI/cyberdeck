import tkinter as tk
from tkinter import messagebox, filedialog
from Applications.file_viewer import file_viewer

import os

def notepad(main, homepage):
    # Clear the current page
    for widget in main.winfo_children():
        widget.destroy()

    # --- Widgets ---
    button = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="Back"
    )
    button.place(x=20, y=20, width=120, height=80)

    button1 = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="Open"
    )
    button1.place(x=160, y=20, width=120, height=80)

    button2 = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="Save"
    )
    button2.place(x=300, y=20, width=120, height=80)

    text_editor = tk.Text(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2
    )
    text_editor.place(x=20, y=120, width=980, height=460)

    # --- Functions ---
    def open_file(main, homepage):
        file_viewer(main, homepage, lambda path: open_file_callback(main, path))

    def open_file_callback(main, path):
        try:
            with open(path, "r") as file:
                text_editor.delete("1.0", tk.END)
                text_editor.insert("1.0", file.read())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(main, homepage):
        file_viewer(main, homepage, lambda path: save_file_callback(main, path), mode="save")

    def save_file_callback(main, path):
        try:
            with open(path, "w") as file:
                file.write(text_editor.get("1.0", tk.END))
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")


    # --- Button Commands ---
    button.config(command=lambda: homepage(main))
    button.bind("<Return>", lambda e: homepage(main))
    button1.config(command=open_file)
    button1.config(command=lambda: open_file(main, homepage))
    button2.config(command=save_file)
    button2.config(command=lambda: save_file(main, homepage))

    # --- Focus ---
    button.focus_set()
