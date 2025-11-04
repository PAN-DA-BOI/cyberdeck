import tkinter as tk
from homepage import homepage
from utils import on_key
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

# Main window
main = tk.Tk()
main.title("Main Window")
main.config(bg="#000000")
main.geometry("1024x600")

# Bind arrow keys and Escape to the main window
main.bind("<Up>", lambda e: on_key(e, main))
main.bind("<Down>", lambda e: on_key(e, main))
main.bind("<Escape>", lambda e: homepage(main))
main.bind("<Return>", lambda e: None)

# Start with the homepage
homepage(main)
main.mainloop()
