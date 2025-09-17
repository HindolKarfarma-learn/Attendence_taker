import tkinter as tk
from tkinter import *
import os
import cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

def text_to_speech(user_text):
    """Text to speech function with error handling"""
    try:
        engine = pyttsx3.init()
        engine.say(user_text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")


# File paths - using os.path.join for cross-platform compatibility
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join("TrainingImageLabel", "Trainner.yml")

# Create directories if they don't exist
trainimage_path = "./TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

# Ensure TrainingImageLabel directory exists
training_label_dir = os.path.dirname(trainimagelabel_path)
if not os.path.exists(training_label_dir):
    os.makedirs(training_label_dir)

studentdetail_path = "./StudentDetails/studentdetails.csv"
# Ensure StudentDetails directory exists
student_details_dir = os.path.dirname(studentdetail_path)
if not os.path.exists(student_details_dir):
    os.makedirs(student_details_dir)

attendance_path = "Attendance"
if not os.path.exists(attendance_path):
    os.makedirs(attendance_path)

window = Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
window.configure(background="#1c1c1c")  # Dark theme

# Global variable for error screen
sc1 = None

# to destroy screen
def del_sc1():
    global sc1
    if sc1:
        sc1.destroy()
        sc1 = None

# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    try:
        sc1.iconbitmap("AMS.ico")
    except:
        pass  # Icon file might not exist
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",
        font=("Verdana", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

# Load and handle images with error checking
try:
    logo = Image.open("UI_Image/0001.png")
    logo = logo.resize((50, 47), Image.LANCZOS)
    logo1 = ImageTk.PhotoImage(logo)

    titl = tk.Label(window, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
    titl.pack(fill=X)
    l1 = tk.Label(window, image=logo1, bg="#1c1c1c")
    l1.place(x=470, y=10)
except Exception as e:
    print(f"Logo image not found: {e}")
    # Create title without logo
    titl = tk.Label(window, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
    titl.pack(fill=X)

titl = tk.Label(
    window,
    text="AI FACE RECOGNITION",
    bg="#1c1c1c",
    fg="yellow",
    font=("Verdana", 27, "bold")
)
titl.place(x=525, y=12)

a = tk.Label(
    window,
    text="EDU-TECH Attendance System",
    bg="#1c1c1c",
    fg="yellow",
    bd=10,
    font=("Verdana", 35, "bold"),
)
a.pack()

# Load UI images with error handling
def load_ui_image(image_path, position):
    try:
        img = Image.open(image_path)
        img_tk = ImageTk.PhotoImage(img)
        label = Label(window, image=img_tk)
        label.image = img_tk  # Keep a reference
        label.place(x=position[0], y=position[1])
        return label
    except Exception as e:
        print(f"Could not load image {image_path}: {e}")
        return None

# Load UI images
load_ui_image("UI_Image/register.png", (100, 270))
load_ui_image("UI_Image/attendance.png", (980, 270))
load_ui_image("UI_Image/verifyy.png", (600, 270))

def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1c1c1c")
    ImageUI.resizable(0, 0)

    titl = tk.Label(ImageUI, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
    titl.pack(fill=X)

    titl = tk.Label(
        ImageUI,
        text="Register Your Face",
        bg="#1c1c1c",
        fg="green",
        font=("Verdana", 30, "bold")
    )
    titl.place(x=270, y=12)

    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#1c1c1c",
        fg="yellow",
        bd=10,
        font=("Verdana", 24, "bold"),
    )
    a.place(x=280, y=75)

    # Enrollment No
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl1.place(x=120, y=130)

    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl2.place(x=120, y=200)

    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 14, "bold"),
    )
    message.place(x=250, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        try:
            takeImage.TakeImage(
                l1,
                l2,
                haarcasecade_path,
                trainimage_path,
                message,
                err_screen,
                text_to_speech,
            )
            txt1.delete(0, "end")
            txt2.delete(0, "end")
        except Exception as e:
            error_msg = f"Error taking image: {e}"
            message.configure(text=error_msg)
            text_to_speech("Error occurred while taking image")

    def train_image():
        try:
            trainImage.TrainImage(
                haarcasecade_path,
                trainimage_path,
                trainimagelabel_path,
                message,
                text_to_speech,
            )
        except Exception as e:
            error_msg = f"Error training image: {e}"
            message.configure(text=error_msg)
            text_to_speech("Error occurred while training image")

    # Take Image button
    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    takeImg.place(x=130, y=350)

    # Train Image button
    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    trainImg.place(x=360, y=350)

# Main buttons
r = tk.Button(
    window,
    text="Register a new student",
    command=TakeImageUI,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=100, y=520)

def automatic_attedance():
    try:
        automaticAttedance.subjectChoose(text_to_speech)
    except Exception as e:
        text_to_speech("Error occurred in attendance module")
        print(f"Attendance error: {e}")

r = tk.Button(
    window,
    text="Take Attendance",
    command=automatic_attedance,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=600, y=520)

def view_attendance():
    try:
        show_attendance.subjectchoose(text_to_speech)
    except Exception as e:
        text_to_speech("Error occurred while viewing attendance")
        print(f"View attendance error: {e}")

r = tk.Button(
    window,
    text="View Attendance",
    command=view_attendance,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=1000, y=520)

def safe_quit():
    """Safely close the application"""
    try:
        # Close any open CV windows
        cv2.destroyAllWindows()
    except:
        pass
    window.quit()
    window.destroy()

r = tk.Button(
    window,
    text="EXIT",
    bd=10,
    command=safe_quit,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
)
r.place(x=600, y=660)

if __name__ == "__main__":
    window.mainloop()
