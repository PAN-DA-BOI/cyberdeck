import os
import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from bs4 import BeautifulSoup

# Global variables
current_path = os.getcwd()
selected_index = 0
file_list = []
file_frame = None
button_frame = None
text_editor = None
message_box = None
current_widgets = []
search_results = []
selected_result = 0
results_frame = None
content_frame = None
content_text = None

# Main window
main = tk.Tk()
main.title("Main Window")
main.config(bg="#000000")
main.geometry("1024x600")

# Function to clear the current page
def clear_page():
    for widget in main.winfo_children():
        widget.destroy()

# Function to update the file list
def update_file_list():
    global file_list, current_path
    try:
        file_list = [".."] + [f for f in os.listdir(current_path)]
    except Exception as e:
        file_list = [f"Error: {e}"]

# Function to draw the file list
def draw_file_list():
    for widget in file_frame.winfo_children():
        widget.destroy()
    for i, item in enumerate(file_list):
        bg = "#00FF00" if i == selected_index else "#000000"
        name_label = tk.Label(file_frame, text=item, bg=bg, fg="#00FF00", font=("Arial", 10), anchor="w")
        name_label.place(relx=0, rely=i/10, relwidth=0.7, height=40)
        if item == "..":
            type_text = "Parent Directory"
        elif os.path.isdir(os.path.join(current_path, item)):
            type_text = "Folder"
        else:
            ext = os.path.splitext(item)[1]
            type_text = ext[1:] if ext else "File"
        type_label = tk.Label(file_frame, text=type_text, bg=bg, fg="#FF00FF", font=("Arial", 10), anchor="e")
        type_label.place(relx=0.7, rely=i/10, relwidth=0.3, height=40)

# Function to read last messages
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

# Function to open a file
def open_file():
    global current_path, selected_index, file_frame, current_widgets, text_editor

    def exit_file_viewer():
        notepad()

    def inner_draw_file_list():
        for widget in file_frame.winfo_children():
            widget.destroy()
        for i, item in enumerate(file_list):
            bg = "#00FF00" if i == selected_index else "#000000"
            name_label = tk.Label(file_frame, text=item, bg=bg, fg="#00FF00", font=("Arial", 10), anchor="w")
            name_label.place(relx=0, rely=i/10, relwidth=0.7, height=40)
            if item == "..":
                type_text = "Parent Directory"
            elif os.path.isdir(os.path.join(current_path, item)):
                type_text = "Folder"
            else:
                ext = os.path.splitext(item)[1]
                type_text = ext[1:] if ext else "File"
            type_label = tk.Label(file_frame, text=type_text, bg=bg, fg="#FF00FF", font=("Arial", 10), anchor="e")
            type_label.place(relx=0.7, rely=i/10, relwidth=0.3, height=40)

    clear_page()
    current_path = os.getcwd()
    selected_index = 0
    update_file_list()

    file_frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    file_frame.place(x=60, y=20, width=800, height=480)

    back_button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Back")
    back_button.place(x=880, y=180, width=120, height=80)

    open_button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Open")
    open_button.place(x=880, y=380, width=120, height=80)

    inner_draw_file_list()

    current_widgets = [back_button, open_button]
    current_widgets[0].focus_set()

    def on_key_file(event):
        nonlocal selected_index, current_path
        if event.keysym == "Right" and selected_index < len(file_list) - 1:
            selected_index += 1
            inner_draw_file_list()
        elif event.keysym == "Left" and selected_index > 0:
            selected_index -= 1
            inner_draw_file_list()
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
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open file: {e}")
            selected_index = 0
            update_file_list()
            inner_draw_file_list()
        elif event.keysym == "Escape":
            exit_file_viewer()

    def on_key_button(event):
        current_index = current_widgets.index(main.focus_get())
        if event.keysym == "Up" and current_index > 0:
            current_widgets[current_index - 1].focus_set()
        elif event.keysym == "Down" and current_index < len(current_widgets) - 1:
            current_widgets[current_index + 1].focus_set()
        elif event.keysym == "Left":
            file_frame.focus_set()
            inner_draw_file_list()
        elif event.keysym == "Escape":
            exit_file_viewer()

    file_frame.bind("<Left>", on_key_file)
    file_frame.bind("<Right>", on_key_file)
    file_frame.bind("<Return>", on_key_file)
    file_frame.bind("<Escape>", lambda e: exit_file_viewer())

    back_button.bind("<Up>", on_key_button)
    back_button.bind("<Down>", on_key_button)
    back_button.bind("<Return>", lambda e: exit_file_viewer())
    back_button.bind("<Left>", lambda e: file_frame.focus_set())
    back_button.bind("<Escape>", lambda e: exit_file_viewer())

    open_button.bind("<Up>", on_key_button)
    open_button.bind("<Down>", on_key_button)
    open_button.bind("<Return>", lambda e: file_frame.focus_set())
    open_button.bind("<Left>", lambda e: file_frame.focus_set())
    open_button.bind("<Escape>", lambda e: exit_file_viewer())

    file_frame.focus_set()

# Function to save a file
def save_file():
    global current_path, selected_index, file_frame, current_widgets, text_editor

    def exit_save_dialog():
        notepad()

    def inner_draw_file_list():
        for widget in file_frame.winfo_children():
            widget.destroy()
        for i, item in enumerate(file_list):
            bg = "#00FF00" if i == selected_index else "#000000"
            name_label = tk.Label(file_frame, text=item, bg=bg, fg="#00FF00", font=("Arial", 10), anchor="w")
            name_label.place(relx=0, rely=i/10, relwidth=0.7, height=40)
            if item == "..":
                type_text = "Parent Directory"
            elif os.path.isdir(os.path.join(current_path, item)):
                type_text = "Folder"
            else:
                ext = os.path.splitext(item)[1]
                type_text = ext[1:] if ext else "File"
            type_label = tk.Label(file_frame, text=type_text, bg=bg, fg="#FF00FF", font=("Arial", 10), anchor="e")
            type_label.place(relx=0.7, rely=i/10, relwidth=0.3, height=40)

    def save_current_file():
        filename = filename_entry.get().strip()
        if filename:
            full_path = os.path.join(current_path, filename)
            try:
                with open(full_path, "w") as file:
                    content = text_editor.get("1.0", tk.END)
                    file.write(content)
                messagebox.showinfo("Success", f"File saved as {filename}")
                notepad()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            messagebox.showwarning("Warning", "Please enter a filename")

    clear_page()
    current_path = os.getcwd()
    selected_index = 0
    update_file_list()

    file_frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    file_frame.place(x=60, y=20, width=800, height=400)

    filename_frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    filename_frame.place(x=60, y=430, width=800, height=40)

    filename_label = tk.Label(filename_frame, text="Filename:", bg="#000000", fg="#00FF00", font=("Arial", 10))
    filename_label.place(relx=0, rely=0, relwidth=0.2, height=40)

    filename_entry = tk.Entry(filename_frame, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=1)
    filename_entry.place(relx=0.2, rely=0, relwidth=0.7, height=40)
    filename_entry.delete(0, tk.END)
    filename_entry.insert(0, "untitled.txt")

    button_frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    button_frame.place(x=60, y=480, width=800, height=40)

    back_button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Back")
    back_button.place(x=880, y=180, width=120, height=80)

    save_button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Save")
    save_button.place(x=880, y=380, width=120, height=80)

    inner_draw_file_list()

    current_widgets = [back_button, save_button, filename_entry, file_frame]
    filename_entry.focus_set()

    def on_key_file(event):
        nonlocal selected_index, current_path
        if event.keysym == "Right" and selected_index < len(file_list) - 1:
            selected_index += 1
            inner_draw_file_list()
        elif event.keysym == "Left" and selected_index > 0:
            selected_index -= 1
            inner_draw_file_list()
        elif event.keysym == "Return":
            selected_item = file_list[selected_index]
            if selected_item == "..":
                current_path = os.path.dirname(current_path)
            elif os.path.isdir(os.path.join(current_path, selected_item)):
                current_path = os.path.join(current_path, selected_item)
            selected_index = 0
            update_file_list()
            inner_draw_file_list()
        elif event.keysym == "Escape":
            exit_save_dialog()

    def on_key_entry(event):
        if event.keysym == "Escape":
            exit_save_dialog()
        elif event.keysym == "Return":
            save_current_file()

    def on_key_button(event):
        current_index = current_widgets.index(main.focus_get())
        if event.keysym == "Up" and current_index > 0:
            current_widgets[current_index - 1].focus_set()
        elif event.keysym == "Down" and current_index < len(current_widgets) - 1:
            current_widgets[current_index + 1].focus_set()
        elif event.keysym == "Left":
            file_frame.focus_set()
            inner_draw_file_list()
        elif event.keysym == "Escape":
            exit_save_dialog()

    file_frame.bind("<Left>", on_key_file)
    file_frame.bind("<Right>", on_key_file)
    file_frame.bind("<Return>", on_key_file)
    file_frame.bind("<Escape>", lambda e: exit_save_dialog())

    filename_entry.bind("<Escape>", on_key_entry)
    filename_entry.bind("<Return>", lambda e: save_current_file())

    back_button.bind("<Up>", on_key_button)
    back_button.bind("<Down>", on_key_button)
    back_button.bind("<Return>", lambda e: exit_save_dialog())
    back_button.bind("<Left>", lambda e: file_frame.focus_set())
    back_button.bind("<Escape>", lambda e: exit_save_dialog())

    save_button.bind("<Up>", on_key_button)
    save_button.bind("<Down>", on_key_button)
    save_button.bind("<Return>", lambda e: save_current_file())
    save_button.bind("<Left>", lambda e: file_frame.focus_set())
    save_button.bind("<Escape>", lambda e: exit_save_dialog())

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
    button.config(command=homepage)
    button.bind("<Return>", lambda e: homepage())
    button1.config(command=open_file)
    button1.bind("<Return>", lambda e: open_file())
    button2.config(command=save_file)
    button2.bind("<Return>", lambda e: save_file())

# Function to send a message
def send_msg_meshtastic():
    global message_box
    message = message_box.get("1.0", tk.END).strip()
    if message:
        with open("./meshtastic/log.txt", "a") as log_file:
            log_file.write(f'\nout-"{message}"')
        print(f"Sending message: {message}")
        message_box.delete("1.0", tk.END)
        comms()
    else:
        print("Empty Message, Please enter a message.")

# Function to set up the comms page
def comms():
    clear_page()
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
    button.config(command=homepage)
    button.bind("<Return>", lambda e: homepage())
    button1.config(command=send_msg_meshtastic)
    button1.bind("<Return>", lambda e: send_msg_meshtastic())

def fetch_search_results(query):
    """Fetch search results from a search engine (example uses a mock response)."""
    mock_results = [
        {"title": "Example Domain", "url": "https://example.com", "description": "This domain is for use in illustrative examples in documents."},
        {"title": "Python Official Site", "url": "https://python.org", "description": "The official home of the Python Programming Language."},
        {"title": "GitHub", "url": "https://github.com", "description": "Where the world builds software."},
    ]
    return mock_results

def fetch_website_content(url):
    """Fetch and strip a website to its raw text."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for element in soup(['script', 'style', 'img', 'nav', 'footer', 'iframe', 'link', 'meta']):
            element.decompose()
        text = soup.get_text(separator='\n', strip=True)
        return text
    except Exception as e:
        return f"Failed to fetch content: {e}"

def display_search_results():
    """Display search results in the results frame."""
    for widget in results_frame.winfo_children():
        widget.destroy()
    for i, result in enumerate(search_results):
        bg = "#00FF00" if i == selected_result else "#000000"
        title_label = tk.Label(results_frame, text=result["title"], bg=bg, fg="#00FF00", font=("Arial", 12, "bold"), anchor="w")
        title_label.place(relx=0, rely=i/10, relwidth=1.0, height=25)
        desc_label = tk.Label(results_frame, text=result["description"], bg=bg, fg="#AAAAAA", font=("Arial", 10), anchor="w")
        desc_label.place(relx=0, rely=(i/10) + 0.03, relwidth=1.0, height=20)

def display_website_content(url):
    """Display the stripped content of a website."""
    content = fetch_website_content(url)
    content_text.delete("1.0", tk.END)
    content_text.insert("1.0", content)

def browser_search():
    """Open the browser search page."""
    clear_page()
    global search_results, selected_result, results_frame, content_frame, content_text, current_widgets

    search_query = tk.StringVar()

    query_frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    query_frame.place(x=20, y=20, width=980, height=60)

    query_label = tk.Label(query_frame, text="Search:", bg="#000000", fg="#00FF00", font=("Arial", 12))
    query_label.place(relx=0, rely=0, relwidth=0.15, height=50)

    query_entry = tk.Entry(query_frame, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=1, textvariable=search_query, font=("Arial", 12))
    query_entry.place(relx=0.15, rely=0, relwidth=0.7, height=50)

    search_button = tk.Button(query_frame, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Search", font=("Arial", 12))
    search_button.place(relx=0.85, rely=0, relwidth=0.15, height=50)

    results_frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    results_frame.place(x=20, y=100, width=980, height=300)

    content_frame = tk.Frame(master=main, bg="#000000", highlightbackground="#00FF00", highlightthickness=2)
    content_frame.place(x=20, y=420, width=980, height=150)

    content_text = tk.Text(content_frame, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, font=("Arial", 10))
    content_text.place(x=0, y=0, width=980, height=150)

    back_button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Back", font=("Arial", 12))
    back_button.place(x=20, y=580, width=120, height=50)

    def on_search():
        """Handle search button press."""
        nonlocal search_results, selected_result
        query = search_query.get()
        search_results = fetch_search_results(query)
        selected_result = 0
        display_search_results()

    def on_key_results(event):
        """Handle key events for the results frame."""
        nonlocal selected_result
        if event.keysym == "Up" and selected_result > 0:
            selected_result -= 1
            display_search_results()
        elif event.keysym == "Down" and selected_result < len(search_results) - 1:
            selected_result += 1
            display_search_results()
        elif event.keysym == "Return":
            selected_url = search_results[selected_result]["url"]
            display_website_content(selected_url)

    def on_key_button(event):
        """Handle key events for the buttons."""
        if event.keysym == "Escape":
            homepage()

    search_button.config(command=on_search)
    search_button.bind("<Return>", lambda e: on_search())

    back_button.config(command=homepage)
    back_button.bind("<Return>", lambda e: homepage())

    results_frame.bind("<Up>", on_key_results)
    results_frame.bind("<Down>", on_key_results)
    results_frame.bind("<Return>", lambda e: display_website_content(search_results[selected_result]["url"]))

    back_button.bind("<Escape>", on_key_button)

    current_widgets = [query_entry, search_button, results_frame, back_button]
    current_widgets[0].focus_set()

    query_entry.focus_set()

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
    label1 = tk.Label(button1, text="COMMS", bg="#000000", fg="#00FF00", font=("Arial", 12))
    label1.place(relx=0.5, rely=0.5, anchor="center")
    browser_button = tk.Button(master=main, bg="#000000", fg="#00FF00", highlightbackground="#00FF00", highlightthickness=2, text="Browser")
    browser_button.place(x=20, y=300, width=980, height=120)
    label2 = tk.Label(browser_button, text="Browser", bg="#000000", fg="#00FF00", font=("Arial", 12))
    label2.place(relx=0.5, rely=0.5, anchor="center")
    current_widgets = [button, button1, browser_button]
    current_widgets[0].focus_set()
    button.config(command=notepad)
    button.bind("<Return>", lambda e: notepad())
    button1.bind("<Return>", lambda e: comms())
    browser_button.config(command=browser_search)
    browser_button.bind("<Return>", lambda e: browser_search())

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
main.bind("<Return>", lambda e: None)

# Start with the homepage
homepage()
main.mainloop()
