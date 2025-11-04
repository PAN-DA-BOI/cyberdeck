import tkinter as tk
from utils import clear_page, update_file_list
from globals import *


def comms(main,homepage):
    clear_page(main)
    global current_widgets, message_box
    button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Back")
    button.place(x=20, y=20, width=120, height=80)
    frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    frame.place(x=20, y=120, width=980, height=350)
    log_file = "./meshtastic/log.txt"
    messages = read_last_messages(log_file, 10)
    for i, msg in enumerate(messages):
        if msg.startswith('in-'):
            text = msg[4:-1]
            label = tk.Label(frame, text=text, bg="#000000", fg="#00FFFF", font=("Arial", 10), anchor="w", justify="left")
            label.place(relx=0.02, rely=i/10, relwidth=0.48, height=35)
        elif msg.startswith('out-'):
            text = msg[5:-1]
            label = tk.Label(frame, text=text, bg="#000000", fg="#00FF00", font=("Arial", 10), anchor="e", justify="right")
            label.place(relx=0.52, rely=i/10, relwidth=0.48, height=35)
    message_box = tk.Text(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2)
    message_box.place(x=20, y=490, width=870, height=80)
    button1 = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Send")
    button1.place(x=900, y=490, width=120, height=80)
    current_widgets = [button, message_box, button1]
    current_widgets[0].focus_set()
    button.config(command=lambda: homepage(main))
    button.bind("<Return>", lambda e: homepage(main))
    button1.config(command=send_msg_meshtastic)
    button1.bind("<Return>", lambda e: send_msg_meshtastic())

def send_msg_meshtastic():
    global message_box
    message = message_box.get("1.0", tk.END).strip()
    if message:
        with open("../meshtastic/log.txt", "a") as log_file:
            log_file.write(f'\nout-"{message}"')
        print(f"Sending message: {message}")
        message_box.delete("1.0", tk.END)
        comms()
    else:
        print("Empty Message, Please enter a message.")
        
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