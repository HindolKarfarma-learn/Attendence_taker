# import tkinter as tk
# from tkinter import *
# import os, cv2
# import shutil
# import csv
# import numpy as np
# from PIL import ImageTk, Image
# import pandas as pd
# import datetime
# import time
# import tkinter.ttk as tkk
# import tkinter.font as font
# import subprocess
# import sys
# import os

# def open_folder(path):
#     if sys.platform.startswith('darwin'):      # macOS
#         subprocess.call(['open', path])
#     elif os.name == 'nt':                      # Windows
#         os.startfile(path)
#     elif os.name == 'posix':                   # Linux
#         subprocess.call(['xdg-open', path])


# haarcasecade_path = "haarcascade_frontalface_default.xml"
# trainimagelabel_path = os.path.join("TrainingImageLabel", "Trainner.yml")

# trainimage_path = "TrainingImage"
# studentdetail_path = os.path.join("StudentDetails", "studentdetails.csv")

# attendance_path = "Attendance"
# # for choose subject and fill attendance
# def subjectChoose(text_to_speech):
#     def FillAttendance():
#         sub = tx.get()
#         now = time.time()
#         future = now + 20
#         print(now)
#         print(future)
#         if sub == "":
#             t = "Please enter the subject name!!!"
#             text_to_speech(t)
#         else:
#             try:
#                 recognizer = cv2.face.LBPHFaceRecognizer_create()
#                 try:
#                     recognizer.read(trainimagelabel_path)
#                 except:
#                     e = "Model not found,please train model"
#                     Notifica.configure(
#                         text=e,
#                         bg="black",
#                         fg="yellow",
#                         width=33,
#                         font=("times", 15, "bold"),
#                     )
#                     Notifica.place(x=20, y=250)
#                     text_to_speech(e)
#                 facecasCade = cv2.CascadeClassifier(haarcasecade_path)
#                 df = pd.read_csv(studentdetail_path)
#                 cam = cv2.VideoCapture(0)
#                 font = cv2.FONT_HERSHEY_SIMPLEX
#                 col_names = ["Enrollment", "Name"]
#                 attendance = pd.DataFrame(columns=col_names)
#                 while True:
#                     ___, im = cam.read()
#                     gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#                     faces = facecasCade.detectMultiScale(gray, 1.2, 5)
#                     for (x, y, w, h) in faces:
#                         global Id

#                         Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
#                         if conf < 70:
#                             print(conf)
#                             global Subject
#                             global aa
#                             global date
#                             global timeStamp
#                             Subject = tx.get()
#                             ts = time.time()
#                             date = datetime.datetime.fromtimestamp(ts).strftime(
#                                 "%Y-%m-%d"
#                             )
#                             timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
#                                 "%H:%M:%S"
#                             )
#                             aa = df.loc[df["Enrollment"] == Id]["Name"].values[0]
#                             global tt
#                             tt = f"{Id}-{aa}"
#                             # En='1604501160'+str(Id)
#                             attendance.loc[len(attendance)] = [
#                                 Id,
#                                 aa,
#                             ]
#                             cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
#                             cv2.putText(
#                                 im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
#                             )
#                         else:
#                             Id = "Unknown"
#                             tt = str(Id)
#                             cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
#                             cv2.putText(
#                                 im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
#                             )
#                     if time.time() > future:
#                         break

#                     attendance = attendance.drop_duplicates(
#                         ["Enrollment"], keep="first"
#                     )
#                     cv2.imshow("Filling Attendance...", im)
#                     key = cv2.waitKey(30) & 0xFF
#                     if key == 27:
#                         break

#                 ts = time.time()
#                 print(aa)
#                 # attendance["date"] = date
#                 # attendance["Attendance"] = "P"
#                 attendance[date] = 1
#                 date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
#                 timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
#                 Hour, Minute, Second = timeStamp.split(":")
#                 # fileName = "Attendance/" + Subject + ".csv"
#                 path = os.path.join(attendance_path, Subject)
#                 if not os.path.exists(path):
#                     os.makedirs(path)
#                 fileName = (
#                     f"{path}/"
#                     + Subject
#                     + "_"
#                     + date
#                     + "_"
#                     + Hour
#                     + "-"
#                     + Minute
#                     + "-"
#                     + Second
#                     + ".csv"
#                 )
#                 attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
#                 print(attendance)
#                 attendance.to_csv(fileName, index=False)

#                 m = "Attendance Filled Successfully of " + Subject
#                 Notifica.configure(
#                     text=m,
#                     bg="black",
#                     fg="yellow",
#                     width=33,
#                     relief=RIDGE,
#                     bd=5,
#                     font=("times", 15, "bold"),
#                 )
#                 text_to_speech(m)

#                 Notifica.place(x=20, y=250)

#                 cam.release()
#                 cv2.destroyAllWindows()

#                 import csv
#                 import tkinter

#                 root = tkinter.Tk()
#                 root.title("Attendance of " + Subject)
#                 root.configure(background="black")
#                 cs = os.path.join(path, fileName)
#                 print(cs)
#                 with open(fileName, newline="") as file:
#                     reader = csv.reader(file)
#                     r = 0

#                     for col in reader:
#                         c = 0
#                         for row in col:

#                             label = tkinter.Label(
#                                 root,
#                                 width=10,
#                                 height=1,
#                                 fg="yellow",
#                                 font=("times", 15, " bold "),
#                                 bg="black",
#                                 text=row,
#                                 relief=tkinter.RIDGE,
#                             )
#                             label.grid(row=r, column=c)
#                             c += 1
#                         r += 1
#                 root.mainloop()
#                 print(attendance)
#             except:
#                 f = "No Face found for attendance"
#                 text_to_speech(f)
#                 cv2.destroyAllWindows()

#     ###windo is frame for subject chooser
#     subject = Tk()
#     # windo.iconbitmap("AMS.ico")
#     subject.title("Subject...")
#     subject.geometry("580x320")
#     subject.resizable(0, 0)
#     subject.configure(background="black")
#     # subject_logo = Image.open("UI_Image/0004.png")
#     # subject_logo = subject_logo.resize((50, 47), Image.ANTIALIAS)
#     # subject_logo1 = ImageTk.PhotoImage(subject_logo)
#     titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
#     titl.pack(fill=X)
#     # l1 = tk.Label(subject, image=subject_logo1, bg="black",)
#     # l1.place(x=100, y=10)
#     titl = tk.Label(
#         subject,
#         text="Enter the Subject Name",
#         bg="black",
#         fg="green",
#         font=("arial", 25),
#     )
#     titl.place(x=160, y=12)
#     Notifica = tk.Label(
#         subject,
#         text="Attendance filled Successfully",
#         bg="yellow",
#         fg="black",
#         width=33,
#         height=2,
#         font=("times", 15, "bold"),
#     )

#     def Attf():
#         sub = tx.get()
#         if sub == "":
#             t = "Please enter the subject name!!!"
#             text_to_speech(t)
#         else:
#             open_folder(
#                 os.path.join("Attendance", sub)
#             )

#     attf = tk.Button(
#         subject,
#         text="Check Sheets",
#         command=Attf,
#         bd=7,
#         font=("times new roman", 15),
#         bg="black",
#         fg="yellow",
#         height=2,
#         width=10,
#         relief=RIDGE,
#     )
#     attf.place(x=360, y=170)

#     sub = tk.Label(
#         subject,
#         text="Enter Subject",
#         width=10,
#         height=2,
#         bg="black",
#         fg="yellow",
#         bd=5,
#         relief=RIDGE,
#         font=("times new roman", 15),
#     )
#     sub.place(x=50, y=100)

#     tx = tk.Entry(
#         subject,
#         width=15,
#         bd=5,
#         bg="black",
#         fg="yellow",
#         relief=RIDGE,
#         font=("times", 30, "bold"),
#     )
#     tx.place(x=190, y=100)

#     fill_a = tk.Button(
#         subject,
#         text="Fill Attendance",
#         command=FillAttendance,
#         bd=7,
#         font=("times new roman", 15),
#         bg="black",
#         fg="yellow",
#         height=2,
#         width=12,
#         relief=RIDGE,
#     )
#     fill_a.place(x=195, y=170)
#     subject.mainloop()
import tkinter as tk
from tkinter import *
import os
import cv2
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font
import subprocess
import sys
import platform

def open_folder(path):
    """Cross-platform folder opening function"""
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        system = platform.system()
        if system == 'Darwin':      # macOS
            subprocess.run(['open', path], check=True)
        elif system == 'Windows':   # Windows
            os.startfile(path)
        else:                       # Linux and other Unix-like systems
            subprocess.run(['xdg-open', path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Could not open folder {path}: subprocess error {e}")
    except Exception as e:
        print(f"Could not open folder {path}: {e}")

# File paths with cross-platform compatibility
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join("TrainingImageLabel", "Trainner.yml")
trainimage_path = "TrainingImage"
studentdetail_path = os.path.join("StudentDetails", "studentdetails.csv")
attendance_path = "Attendance"

# Ensure required directories exist
def ensure_directories():
    """Create required directories if they don't exist"""
    directories = [
        os.path.dirname(trainimagelabel_path),
        trainimage_path,
        os.path.dirname(studentdetail_path),
        attendance_path
    ]

    for directory in directories:
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                print(f"Could not create directory {directory}: {e}")

def subjectChoose(text_to_speech):
    ensure_directories()

    def FillAttendance():
        sub = tx.get().strip()

        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
            return

        # Sanitize subject name for file system
        sub_clean = "".join(c for c in sub if c.isalnum() or c in (' ', '-', '_')).strip()
        sub_clean = sub_clean.replace(' ', '_')

        # Additional validation for minimum length
        if not sub_clean or len(sub_clean.strip('_')) < 2:
            t = "Please enter a valid subject name with at least 2 characters!"
            text_to_speech(t)
            Notifica.configure(
                text=t,
                bg="black",
                fg="red",
                width=40,
                font=("times", 12, "bold"),
            )
            Notifica.place(x=50, y=250)
            return

        # Check if required files exist
        if not os.path.exists(haarcasecade_path):
            e = "Haar cascade file not found. Please ensure haarcascade_frontalface_default.xml is in the project directory."
            Notifica.configure(
                text=e,
                bg="black",
                fg="red",
                width=40,
                font=("times", 12, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech("Haar cascade file not found")
            return

        if not os.path.exists(studentdetail_path):
            e = "Student details file not found. Please register students first."
            Notifica.configure(
                text=e,
                bg="black",
                fg="red",
                width=40,
                font=("times", 12, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech("Student details not found")
            return

        try:
            # Initialize face recognizer
            recognizer = cv2.face.LBPHFaceRecognizer_create()

            try:
                recognizer.read(trainimagelabel_path)
            except Exception as model_error:
                e = "Model not found or corrupted. Please train the model first."
                Notifica.configure(
                    text=e,
                    bg="black",
                    fg="red",
                    width=40,
                    font=("times", 12, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech(e)
                return

            # Load face cascade
            facecasCade = cv2.CascadeClassifier(haarcasecade_path)
            if facecasCade.empty():
                e = "Failed to load face cascade classifier"
                Notifica.configure(
                    text=e,
                    bg="black",
                    fg="red",
                    width=40,
                    font=("times", 12, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech(e)
                return

            # Load student details
            try:
                df = pd.read_csv(studentdetail_path)
                if df.empty:
                    e = "No student records found. Please register students first."
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="red",
                        width=40,
                        font=("times", 12, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                    return
            except Exception as csv_error:
                e = "Error reading student details file"
                Notifica.configure(
                    text=e,
                    bg="black",
                    fg="red",
                    width=40,
                    font=("times", 12, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech(e)
                return

            # Initialize camera
            cam = cv2.VideoCapture(0)
            if not cam.isOpened():
                e = "Camera not accessible. Please check camera connection."
                Notifica.configure(
                    text=e,
                    bg="black",
                    fg="red",
                    width=40,
                    font=("times", 12, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech(e)
                return

            # Set camera properties
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            font_cv = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ["Enrollment", "Name"]
            attendance = pd.DataFrame(columns=col_names)

            # Attendance duration (20 seconds)
            now = time.time()
            future = now + 20

            recognized_students = set()  # Track already recognized students

            print(f"Starting attendance for {sub_clean}...")
            text_to_speech(f"Starting attendance for {sub}")

            while True:
                ret, im = cam.read()
                if not ret:
                    print("Failed to read from camera")
                    break

                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = facecasCade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(30, 30)
                )

                for (x, y, w, h) in faces:
                    Id, conf = recognizer.predict(gray[y : y + h, x : x + w])

                    if conf < 50:  # Good recognition
                        try:
                            # Find student name
                            student_row = df[df["Enrollment"] == Id]
                            if not student_row.empty:
                                name = student_row["Name"].values[0]
                                display_text = f"{Id}-{name}"

                                # Add to attendance if not already present
                                if Id not in recognized_students:
                                    attendance.loc[len(attendance)] = [Id, name]
                                    recognized_students.add(Id)
                                    print(f"Recognized: {display_text}")

                                # Green rectangle for recognized face
                                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
                                cv2.putText(im, display_text, (x, y-10), font_cv, 0.8, (0, 255, 0), 2)
                            else:
                                # Student not in database
                                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 165, 255), 3)
                                cv2.putText(im, f"ID:{Id} Not Found", (x, y-10), font_cv, 0.8, (0, 165, 255), 2)
                        except Exception as recog_error:
                            print(f"Recognition error: {recog_error}")
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 165, 255), 3)
                            cv2.putText(im, "Error", (x, y-10), font_cv, 0.8, (0, 165, 255), 2)

                    elif conf < 85:  # Uncertain recognition
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 255), 3)
                        cv2.putText(im, "Uncertain", (x, y-10), font_cv, 0.8, (0, 255, 255), 2)

                    else:  # Unknown face
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 3)
                        cv2.putText(im, "Unknown", (x, y-10), font_cv, 0.8, (0, 0, 255), 2)

                # Show timer and instructions
                remaining_time = max(0, int(future - time.time()))
                cv2.putText(im, f"Time: {remaining_time}s", (10, 30), font_cv, 1, (255, 255, 255), 2)
                cv2.putText(im, f"Recognized: {len(recognized_students)}", (10, 70), font_cv, 1, (255, 255, 255), 2)
                cv2.putText(im, "Press ESC to stop", (10, im.shape[0] - 10), font_cv, 0.7, (255, 255, 255), 2)

                cv2.imshow("Taking Attendance - Press ESC to stop", im)

                # Check for exit conditions
                key = cv2.waitKey(30) & 0xFF
                if key == 27:  # ESC key
                    break
                elif time.time() > future:
                    break

            cam.release()
            cv2.destroyAllWindows()

            if attendance.empty:
                f = "No faces recognized for attendance"
                Notifica.configure(
                    text=f,
                    bg="black",
                    fg="red",
                    width=40,
                    font=("times", 12, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech(f)
                return

            # Remove duplicates and prepare final attendance
            attendance = attendance.drop_duplicates(["Enrollment"], keep="first")

            # Add timestamp and date columns
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

            attendance[date] = 1  # Mark as present

            # Create subject folder
            subject_path = os.path.join(attendance_path, sub_clean)
            os.makedirs(subject_path, exist_ok=True)

            # Create filename with timestamp
            hour, minute, second = timeStamp.split(":")
            fileName = os.path.join(
                subject_path,
                f"{sub_clean}_{date}_{hour}-{minute}-{second}.csv"
            )

            # Save attendance file
            try:
                attendance.to_csv(fileName, index=False)
                print(f"Attendance saved to: {fileName}")
            except Exception as save_error:
                e = f"Error saving attendance file: {save_error}"
                Notifica.configure(
                    text=e,
                    bg="black",
                    fg="red",
                    width=40,
                    font=("times", 12, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech("Error saving attendance file")
                return

            # Success message
            m = f"Attendance filled successfully for {sub}. {len(attendance)} students recorded."
            Notifica.configure(
                text=m,
                bg="black",
                fg="green",
                width=40,
                relief=RIDGE,
                bd=5,
                font=("times", 12, "bold"),
            )
            text_to_speech(f"Attendance completed for {sub}")
            Notifica.place(x=20, y=250)

            # Display attendance in new window
            display_attendance_window(fileName, sub)

        except Exception as e:
            error_msg = f"Unexpected error occurred during attendance capture"
            Notifica.configure(
                text=error_msg,
                bg="black",
                fg="red",
                width=40,
                font=("times", 12, "bold"),
            )
            Notifica.place(x=50, y=250)
            text_to_speech("An unexpected error occurred")
            print(f"Full error details: {e}")

            # Cleanup
            try:
                cv2.destroyAllWindows()
                if 'cam' in locals():
                    cam.release()
            except:
                pass

    def display_attendance_window(fileName, subject_name):
        """Display attendance in a new window"""
        try:
            root = tk.Tk()
            root.title(f"Attendance of {subject_name}")
            root.configure(background="black")
            root.geometry("800x600")

            # Create scrollable frame
            canvas = tk.Canvas(root, bg="black")
            scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="black")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Read and display CSV data
            with open(fileName, newline="", encoding='utf-8') as file:
                reader = csv.reader(file)
                row_num = 0

                for row_data in reader:
                    col_num = 0
                    for cell_data in row_data:
                        label = tk.Label(
                            scrollable_frame,
                            width=15,
                            height=2,
                            fg="yellow",
                            font=("times", 12, "bold"),
                            bg="black",
                            text=str(cell_data),
                            relief=tk.RIDGE,
                            bd=1
                        )
                        label.grid(row=row_num, column=col_num, padx=1, pady=1)
                        col_num += 1
                    row_num += 1

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Add close button
            close_btn = tk.Button(
                root,
                text="Close",
                command=root.destroy,
                bg="red",
                fg="white",
                font=("times", 12, "bold")
            )
            close_btn.pack(side="bottom", pady=10)

            root.mainloop()

        except Exception as e:
            print(f"Error displaying attendance window: {e}")

    # Create subject selection window
    subject = Tk()
    subject.title("Subject Selection")
    subject.geometry("600x350")
    subject.resizable(0, 0)
    subject.configure(background="black")

    # Title
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=150, y=12)

    # Notification label
    Notifica = tk.Label(
        subject,
        text="",
        bg="black",
        fg="yellow",
        width=40,
        height=3,
        font=("times", 12, "bold"),
    )

    def check_attendance_folder():
        """Open attendance folder for the subject"""
        sub = tx.get().strip()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
            return

        # Sanitize subject name
        sub_clean = "".join(c for c in sub if c.isalnum() or c in (' ', '-', '_')).strip()
        sub_clean = sub_clean.replace(' ', '_')

        folder_path = os.path.join(attendance_path, sub_clean)
        open_folder(folder_path)

    # Buttons and input fields
    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=check_attendance_folder,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    attf.place(x=380, y=170)

    sub_label = tk.Label(
        subject,
        text="Enter Subject",
        width=12,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub_label.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=20,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 20, "bold"),
    )
    tx.place(x=200, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=14,
        relief=RIDGE,
    )
    fill_a.place(x=200, y=170)

    # Place notification label
    Notifica.place(x=50, y=250)

    subject.mainloop()
