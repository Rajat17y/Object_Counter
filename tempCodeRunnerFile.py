import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import CarCounter as cc
from LinesVid import get_line_coordinates

#Variables
limit_ = []

# ---------- Placeholder for object counter logic ----------
def draw_line_mode():
    global limit_
    print("Line drawing mode activated")
    limit_ = get_line_coordinates(selected_source.get())
    print(limit_)
    # You'd launch your line drawing OpenCV logic here

def start_counting():
    print("Counting started")
    cc.car(selected_source.get(),limit_)
    # You'd launch your object counting logic here

def browse_video():
    filepath = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
    )
    selected_source.set(filepath)
    print(selected_source.get())

def on_source_change(event):
    source = source_choice.get()
    if source == "Webcam":
        selected_source.set("0")  # Default webcam
    elif source == "Browse Video":
        browse_video()

# ---------- GUI Setup ----------
app = tk.Tk()
app.title("Object Counter GUI")
app.geometry("400x250")
app.resizable(False, False)

# Title
tk.Label(app, text="Object Counter", font=("Helvetica", 16, "bold")).pack(pady=10)

# Video Source Selection
tk.Label(app, text="Select Video Source:").pack()
source_choice = ttk.Combobox(app, values=["Webcam", "Browse Video"])
source_choice.current(0)
source_choice.bind("<<ComboboxSelected>>", on_source_change)
source_choice.pack(pady=5)

selected_source = tk.StringVar(value="0")  # Default to webcam

# Draw Line Button
draw_btn = tk.Button(app, text="Draw Line", font=("Helvetica", 12), width=20, command=draw_line_mode)
draw_btn.pack(pady=10)

# Count Button
count_btn = tk.Button(app, text="Start Counting", font=("Helvetica", 12), width=20, command=start_counting)
count_btn.pack(pady=10)

# Run GUI loop
app.mainloop()
