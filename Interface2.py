import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import CarCounter as cc
from LinesVid import get_line_coordinates

# Variables
limit_ = []
#selected_object = tk.StringVar(value="Car")  # Default object type
#selected_source = tk.StringVar(value="0")    # Default to webcam

# ---------- Function Definitions ----------
def draw_line_mode():
    global limit_
    print("Line drawing mode activated")
    limit_ = get_line_coordinates(selected_source.get())
    print(limit_)

def start_counting():
    print("Counting started")
    cc.car(selected_source.get(),limit_,selected_object.get())
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
        selected_source.set("0")
    elif source == "Browse Video":
        browse_video()

# ---------- GUI Setup ----------
app = tk.Tk()
app.title("Object Counter GUI")
app.geometry("400x300")
app.resizable(False, False)

# Now it's safe to create Tkinter variables
selected_object = tk.StringVar(value="Car")  # Default object type
selected_source = tk.StringVar(value="0")    # Default to webcam

# Title
tk.Label(app, text="Object Counter", font=("Helvetica", 16, "bold")).pack(pady=10)

# Video Source Selection
tk.Label(app, text="Select Video Source:").pack()
source_choice = ttk.Combobox(app, values=["Webcam", "Browse Video"])
source_choice.current(0)
source_choice.bind("<<ComboboxSelected>>", on_source_change)
source_choice.pack(pady=5)

# Object Type Selection (Placed directly below source selection)
tk.Label(app, text="What to Count:").pack()
object_choice = ttk.Combobox(app, values=["Car", "People"], textvariable=selected_object)
object_choice.current(0)
object_choice.pack(pady=5)

# Draw Line Button
draw_btn = tk.Button(app, text="Draw Line", font=("Helvetica", 12), width=20, command=draw_line_mode)
draw_btn.pack(pady=10)

# Count Button
count_btn = tk.Button(app, text="Start Counting", font=("Helvetica", 12), width=20, command=start_counting)
count_btn.pack(pady=10)

# Run GUI loop
app.mainloop()
