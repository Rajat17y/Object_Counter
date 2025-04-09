import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk  # For background image support
import CarCounter as cc
from LinesVid import get_line_coordinates

# ---------- Variables ----------
limit_ = []

# ---------- Function Definitions ----------
def draw_line_mode():
    global limit_
    print("Line drawing mode activated")
    limit_ = get_line_coordinates(selected_source.get())
    print(limit_)

def start_counting():
    print("Counting started")
    cc.car(selected_source.get(), limit_, selected_object.get())

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
app.title("🎯 Object Counter")
app.geometry("600x400")
app.resizable(False, False)

# Variables after root creation
selected_object = tk.StringVar(value="Car")
selected_source = tk.StringVar(value="0")

# ---------- Background Image ----------
bg_image = Image.open("4232288.jpg")  # Replace with your background image
bg_image = bg_image.resize((600, 400), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(app, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ---------- Transparent Frame for Content ----------
frame = tk.Frame(app, bg='#ffffff', bd=2, relief='groove')
frame.place(relx=0.5, rely=0.5, anchor='center')

# ---------- UI Elements ----------
tk.Label(frame, text="🎯 Object Counter", font=("Segoe UI", 20, "bold"), bg="#ffffff", fg="#333").pack(pady=10)

tk.Label(frame, text="Select Video Source:", font=("Segoe UI", 12), bg="#ffffff").pack()
source_choice = ttk.Combobox(frame, values=["Webcam", "Browse Video"], font=("Segoe UI", 10))
source_choice.current(0)
source_choice.bind("<<ComboboxSelected>>", on_source_change)
source_choice.pack(pady=5)

tk.Label(frame, text="What to Count:", font=("Segoe UI", 12), bg="#ffffff").pack()
object_choice = ttk.Combobox(frame, values=["Car", "People"], textvariable=selected_object, font=("Segoe UI", 10))
object_choice.current(0)
object_choice.pack(pady=5)

draw_btn = tk.Button(frame, text="✏️ Draw Line", font=("Segoe UI", 12), bg="#4CAF50", fg="white", width=20, command=draw_line_mode)
draw_btn.pack(pady=10)

count_btn = tk.Button(frame, text="📊 Start Counting", font=("Segoe UI", 12), bg="#2196F3", fg="white", width=20, command=start_counting)
count_btn.pack(pady=10)

# ---------- Run GUI ----------
app.mainloop()
