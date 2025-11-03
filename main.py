import tkinter as tk
from tkinter import filedialog
import tkinter as tk

current_path = os.getcwd()
selected_index = 0
file_list = []
file_frame = None
button_frame = None


main = tk.Tk()
main.title("Main Window")
main.config(bg="#000000")
main.geometry("1024x600")

# Global variable to track current interactive widgets
current_widgets = []
text_editor = None


def update_file_list():
    global file_list, selected_index
    try:
        file_list = [".."] + [f for f in os.listdir(current_path)]
    except Exception as e:
        file_list = [f"Error: {e}"]

def draw_file_list():
    global file_frame, selected_index
    for widget in file_frame.winfo_children():
        widget.destroy()
    for i, item in enumerate(file_list):
        bg = "#00FF00" if i == selected_index else "#000000"
        label = tk.Label(file_frame, text=item, bg=bg, fg="#00FF00", font=("Arial", 10), anchor="w")
        label.place(relx=0, rely=i/10, relwidth=1.0, height=40)



# Function to clear the current page
def clear_page():
    for widget in main.winfo_children():
        widget.destroy()
def read_last_messages(log_file, num_messages=10):
    try:
        with open(log_file, "r") as file:
            lines = file.readlines()
        # Extract the last 'num_messages' lines
        last_messages = lines[-num_messages:] if len(lines) >= num_messages else lines
        return [line.strip() for line in last_messages]
    except FileNotFoundError:
        return ["No log file found."]
    except Exception as e:
        return [f"Error reading log: {e}"]
        

# Function to open a file
def open_file():
    global current_path, selected_index, file_frame, button_frame, current_widgets
    clear_page()
    current_path = os.getcwd()
    selected_index = 0
    update_file_list()

    file_frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    file_frame.place(x=60, y=20, width=800, height=480)

    button_frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    button_frame.place(x=60, y=490, width=800, height=40)

    back_button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Back")
    back_button.place(x=880, y=180, width=120, height=80)

    open_button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Open")
    open_button.place(x=880, y=380, width=120, height=80)

    draw_file_list()

    current_widgets = [back_button, file_frame, open_button]
    current_widgets[0].focus_set()

    def on_key_file(event):
        global selected_index, current_path
        nonlocal file_list
        if event.keysym == "Up" and selected_index > 0:
            selected_index -= 1
            draw_file_list()
        elif event.keysym == "Down" and selected_index < len(file_list) - 1:
            selected_index += 1
            draw_file_list()
        elif event.keysym == "Return":
            selected_item = file_list[selected_index]
            if selected_item == "..":
                current_path = os.path.dirname(current_path)
            elif os.path.isdir(os.path.join(current_path, selected_item)):
                current_path = os.path.join(current_path, selected_item)
            else:
                try:
                    with open(os.path.join(current_path, selected_item), "r") as file:
                        text_editor.delete("1.0", tk.END)
                        text_editor.insert("1.0", file.read())
                    notepad()
                    return
            selected_index = 0
            update_file_list()
            draw_file_list()
        elif event.keysym == "Right":
            open_button.focus_set()
        elif event.keysym == "Left":
            back_button.focus_set()

    def on_key_button(event):
        if event.keysym == "Left":
            file_frame.focus_set()
            draw_file_list()

    file_frame.bind("<Up>", on_key_file)
    file_frame.bind("<Down>", on_key_file)
    file_frame.bind("<Return>", on_key_file)
    file_frame.bind("<Right>", on_key_file)
    file_frame.bind("<Left>", on_key_file)

    back_button.config(command=notepad)
    back_button.bind("<Return>", lambda e: notepad())
    back_button.bind("<Left>", lambda e: file_frame.focus_set())

    open_button.config(command=lambda: file_frame.focus_set())
    open_button.bind("<Return>", lambda e: file_frame.focus_set())
    open_button.bind("<Left>", lambda e: file_frame.focus_set())

    file_frame.focus_set()
    draw_file_list()

    
# Function to save a file
def save_file():
    global text_editor
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            content = text_editor.get("1.0", tk.END)
            file.write(content)

# Function to set up the notepad page
def notepad():
    clear_page()
    global current_widgets, text_editor
    button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Back")
    button.place(x=20, y=20, width=120, height=80)
    button1 = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Open")
    button1.place(x=160, y=20, width=120, height=80)
    button2 = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Save")
    button2.place(x=300, y=20, width=120, height=80)
    text_editor = tk.Text(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2)
    text_editor.place(x=20, y=120, width=980, height=460)
    current_widgets = [button, button1, button2, text_editor]
    current_widgets[0].focus_set()

    # Bind Enter key to buttons
    button.config(command=homepage)
    button.bind("<Return>", lambda e: homepage())
    button1.config(command=open_file)
    button1.bind("<Return>", lambda e: open_file())
    button2.config(command=save_file)
    button2.bind("<Return>", lambda e: save_file())

def send_msg_meshtastic():
    message = message_box.get("1.0", tk.END).strip()
    if message:
        # Append the message to the log file
        with open("./meshtastic/log.txt", "a") as log_file:
            log_file.write(f'\nout-"{message}"')
        # Replace this with your actual send logic
        print(f"Sending message: {message}")
        # Optionally, refresh the chat display
        comms()
    else:
        print("Empty Message, Please enter a message.")

def comms():
    clear_page()
    global current_widgets, message_box
    button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Back")
    button.place(x=20, y=20, width=120, height=80)
    frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    frame.place(x=20, y=120, width=980, height=350)

    # Display last 10 messages in the frame
    log_file = "./meshtastic/log.txt"
    messages = read_last_messages(log_file, 10)
    for i, msg in enumerate(messages):
        if msg.startswith('in-'):
            # Incoming message (left, blue)
            text = msg[4:-1]  # Remove in-" and "
            label = tk.Label(frame, text=text, bg="#000000", fg="#00FFFF", font=("Arial", 10), anchor="w", justify="left")
            label.place(relx=0.02, rely=i/10, relwidth=0.48, height=35)
        elif msg.startswith('out-'):
            # Outgoing message (right, green)
            text = msg[5:-1]  # Remove out-" and "
            label = tk.Label(frame, text=text, bg="#000000", fg="#00FF00", font=("Arial", 10), anchor="e", justify="right")
            label.place(relx=0.52, rely=i/10, relwidth=0.48, height=35)

    message_box = tk.Text(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2)
    message_box.place(x=20, y=490, width=870, height=80)
    button1 = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Send")
    button1.place(x=900, y=490, width=120, height=80)
    current_widgets = [button, message_box, button1]
    current_widgets[0].focus_set()

    # Bind Enter key to buttons
    button.config(command=homepage)
    button.bind("<Return>", lambda e: homepage())
    button1.config(command=send_msg_meshtastic)
    button1.bind("<Return>", lambda e: send_msg_meshtastic())
    
#def camera_connector
# Function to set up the homepage
def homepage():
    clear_page()
    global current_widgets
    button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Notepad")
    button.place(x=20, y=20, width=980, height=120)
    label = tk.Label(button, text="Notepad", bg="#000000", fg="#00FF00", font=("Arial", 12))
    label.place(relx=0.5, rely=0.5, anchor="center")
    button1 = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="COMMS")
    button1.place(x=20, y=160, width=980, height=120)
    label1 = tk.Label(button1, text="Option 2", bg="#000000", fg="#00FF00", font=("Arial", 12))
    label1.place(relx=0.5, rely=0.5, anchor="center")
    button2 = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Option 3")
    button2.place(x=20, y=300, width=980, height=120)
    label2 = tk.Label(button2, text="Option 3", bg="#000000", fg="#00FF00", font=("Arial", 12))
    label2.place(relx=0.5, rely=0.5, anchor="center")
    current_widgets = [button, button1, button2]
    current_widgets[0].focus_set()

    # Bind Enter key to buttons
    button.config(command=notepad)
    button.bind("<Return>", lambda e: notepad())
    button1.bind("<Return>", lambda e: comms())
    button2.bind("<Return>", lambda e: open_file())

# Function to handle arrow key navigation
def on_key(event):
    try:
        current_index = current_widgets.index(main.focus_get())
        if event.keysym == "Up" and current_index > 0:
            current_widgets[current_index - 1].focus_set()
        elif event.keysym == "Down" and current_index < len(current_widgets) - 1:
            current_widgets[current_index + 1].focus_set()
        elif event.keysym == "Escape":
            homepage()
    except (ValueError, IndexError):
        pass

# Bind arrow keys and Escape to the main window
main.bind("<Up>", on_key)
main.bind("<Down>", on_key)
main.bind("<Escape>", on_key)
main.bind("<Return>", lambda e: None)  # Prevent default behavior for Enter

# Start with the homepage
homepage()

main.mainloop()
