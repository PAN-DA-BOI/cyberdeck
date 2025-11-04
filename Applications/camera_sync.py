import tkinter as tk
import os
import shutil
from tkinter import messagebox

def camera_sync(main, homepage):
    # Clear the current page
    for widget in main.winfo_children():
        widget.destroy()

    # --- Constants ---
    PHOTO_DIR = r"UserFiles\Sable\Photos"
    VIDEO_DIR = r"UserFiles\Sable\Videos"
    SUPPORTED_PHOTO_EXT = ('.jpg', '.jpeg', '.png', '.heic', '.gif', '.bmp')
    SUPPORTED_VIDEO_EXT = ('.mp4', '.mov', '.avi', '.mkv')

    # --- Widgets ---
    title = tk.Label(
        master=main,
        text="Camera Sync",
        bg="#000000",
        fg="#00FF00",
        font=("Arial", 16, "bold")
    )
    title.place(x=20, y=20, width=980, height=40)

    info_label = tk.Label(
        master=main,
        text="Press the button below to download all photos and videos from your camera.",
        bg="#000000",
        fg="#AAAAAA",
        font=("Arial", 12),
        wraplength=900
    )
    info_label.place(x=20, y=80, width=980, height=60)

    sync_button = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="Download All Media"
    )
    sync_button.place(x=20, y=160, width=980, height=120)

    status_label = tk.Label(
        master=main,
        text="Ready.",
        bg="#000000",
        fg="#AAAAAA",
        font=("Arial", 12)
    )
    status_label.place(x=20, y=300, width=980, height=40)

    back_button = tk.Button(
        master=main,
        bg="#000000",
        fg="#00FF00",
        highlightbackground="#00FF00",
        highlightthickness=2,
        text="Back"
    )
    back_button.place(x=20, y=500, width=980, height=80)

    # --- Functions ---
    def update_status(text, is_error=False):
        status_label.config(text=text, fg="#FF0000" if is_error else "#AAAAAA")

    def sync_media():
        try:
            # Find the first connected camera/USB drive (simplified for demo)
            # In a real app, you'd use a library like `pyudev` or `win32api` to detect devices.
            # For now, we'll assume the camera is mounted as a drive letter (e.g., E:)
            camera_path = None
            for drive in "DEFGHIJKLMNOPQRSTUVWXYZ":
                path = f"{drive}:\\"
                if os.path.exists(path):
                    # Check if this drive has DCIM (common for cameras)
                    dcim = os.path.join(path, "DCIM")
                    if os.path.exists(dcim):
                        camera_path = dcim
                        break
            if not camera_path:
                update_status("No camera detected.", is_error=True)
                return

            update_status("Downloading media...")
            photo_count = 0
            video_count = 0

            # Create directories if they don't exist
            os.makedirs(PHOTO_DIR, exist_ok=True)
            os.makedirs(VIDEO_DIR, exist_ok=True)

            # Walk through the camera directory
            for root, _, files in os.walk(camera_path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    src = os.path.join(root, file)
                    if ext in SUPPORTED_PHOTO_EXT:
                        dst = os.path.join(PHOTO_DIR, file)
                        shutil.copy2(src, dst)
                        photo_count += 1
                    elif ext in SUPPORTED_VIDEO_EXT:
                        dst = os.path.join(VIDEO_DIR, file)
                        shutil.copy2(src, dst)
                        video_count += 1

            update_status(f"Done! {photo_count} photos and {video_count} videos downloaded.")
        except Exception as e:
            update_status(f"Error: {e}", is_error=True)

    # --- Bindings ---
    sync_button.config(command=sync_media)
    sync_button.bind("<Return>", lambda e: sync_media())
    back_button.config(command=lambda: homepage(main))
    back_button.bind("<Return>", lambda e: homepage(main))
    main.bind("<Escape>", lambda e: homepage(main))

    # --- Focus ---
    sync_button.focus_set()
