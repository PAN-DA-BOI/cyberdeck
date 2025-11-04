import os
from tkinter import messagebox

def clear_page(main):
    for widget in main.winfo_children():
        widget.destroy()

def update_file_list(current_path):
    try:
        return [".."] + [f for f in os.listdir(current_path)]
    except Exception as e:
        return [f"Error: {e}"]

def read_last_messages(log_file, num_messages=10):
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
        last_messages = lines[-num_messages:] if len(lines) >= num_messages else lines
        return [line.strip() for line in last_messages]
    except FileNotFoundError:
        return ["No log file found."]
    except Exception as e:
        return [f"Error reading log: {e}"]

def on_key(event, main):
    try:
        from globals import current_widgets
        current_index = current_widgets.index(main.focus_get())
        if event.keysym == "Up" and current_index > 0:
            current_widgets[current_index - 1].focus_set()
        elif event.keysym == "Down" and current_index < len(current_widgets) - 1:
            current_widgets[current_index + 1].focus_set()
        elif event.keysym == "Escape":
            from homepage import homepage
            homepage(main)
    except (ValueError, IndexError):
        pass

