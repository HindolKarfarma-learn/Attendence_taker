# import pandas as pd
# from glob import glob
# import os
# import tkinter
# import csv
# import tkinter as tk
# from tkinter import *

# def subjectchoose(text_to_speech):
#     def calculate_attendance():
#         Subject = tx.get()
#         if Subject=="":
#             t='Please enter the subject name.'
#             text_to_speech(t)

#         filenames = glob(
#             f"Attendance\\{Subject}\\{Subject}*.csv"
#         )
#         df = [pd.read_csv(f) for f in filenames]
#         newdf = df[0]
#         for i in range(1, len(df)):
#             newdf = newdf.merge(df[i], how="outer")
#         newdf.fillna(0, inplace=True)
#         newdf["Attendance"] = 0
#         for i in range(len(newdf)):
#             newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100)))+'%'
#             #newdf.sort_values(by=['Enrollment'],inplace=True)
#         newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

#         root = tkinter.Tk()
#         root.title("Attendance of "+Subject)
#         root.configure(background="black")
#         cs = f"Attendance\\{Subject}\\attendance.csv"
#         with open(cs) as file:
#             reader = csv.reader(file)
#             r = 0

#             for col in reader:
#                 c = 0
#                 for row in col:

#                     label = tkinter.Label(
#                         root,
#                         width=10,
#                         height=1,
#                         fg="yellow",
#                         font=("times", 15, " bold "),
#                         bg="black",
#                         text=row,
#                         relief=tkinter.RIDGE,
#                     )
#                     label.grid(row=r, column=c)
#                     c += 1
#                 r += 1
#         root.mainloop()
#         print(newdf)

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
#         text="Which Subject of Attendance?",
#         bg="black",
#         fg="green",
#         font=("arial", 25),
#     )
#     titl.place(x=100, y=12)

#     def Attf():
#         sub = tx.get()
#         if sub == "":
#             t="Please enter the subject name!!!"
#             text_to_speech(t)
#         else:
#             os.startfile(
#             f"Attendance\\{sub}"
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
#         text="View Attendance",
#         command=calculate_attendance,
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
import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *
import subprocess
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

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get().strip()

        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return

        # Sanitize subject name for file system
        Subject_clean = "".join(c for c in Subject if c.isalnum() or c in (' ', '-', '_')).strip()
        Subject_clean = Subject_clean.replace(' ', '_')

        if not Subject_clean:
            t = 'Please enter a valid subject name.'
            text_to_speech(t)
            return

        # Use os.path.join for cross-platform path handling
        attendance_folder = os.path.join("Attendance", Subject_clean)

        if not os.path.exists(attendance_folder):
            t = f'No attendance records found for {Subject}. Please take attendance first.'
            text_to_speech(t)
            return

        try:
            # Cross-platform glob pattern
            pattern = os.path.join("Attendance", Subject_clean, f"{Subject_clean}*.csv")
            filenames = glob(pattern)

            if not filenames:
                t = f'No attendance files found for {Subject}.'
                text_to_speech(t)
                return

            # Read all CSV files
            df_list = []
            for filename in filenames:
                try:
                    df_temp = pd.read_csv(filename)
                    if not df_temp.empty:
                        df_list.append(df_temp)
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")
                    continue

            if not df_list:
                t = f'No valid attendance data found for {Subject}.'
                text_to_speech(t)
                return

            # Start with the first dataframe
            newdf = df_list[0].copy()

            # Merge all dataframes
            for i in range(1, len(df_list)):
                newdf = newdf.merge(df_list[i], on=['Enrollment', 'Name'], how='outer')

            # Fill missing values with 0
            newdf.fillna(0, inplace=True)

            # Calculate attendance percentage
            # Find date columns (exclude Enrollment and Name)
            date_columns = [col for col in newdf.columns if col not in ['Enrollment', 'Name']]

            if date_columns:
                # Calculate attendance percentage for each student
                newdf['Attendance'] = newdf[date_columns].mean(axis=1) * 100
                newdf['Attendance'] = newdf['Attendance'].round(1).astype(str) + '%'
            else:
                # If no date columns, set attendance to 0%
                newdf['Attendance'] = '0%'

            # Sort by enrollment number
            if 'Enrollment' in newdf.columns:
                newdf = newdf.sort_values(by=['Enrollment'])

            # Save consolidated attendance file
            output_file = os.path.join(attendance_folder, "attendance_summary.csv")
            newdf.to_csv(output_file, index=False)

            # Display attendance in a new window
            display_attendance_window(newdf, Subject, output_file)

            print("Attendance calculation completed successfully")
            text_to_speech(f"Attendance calculated for {Subject}")

        except Exception as e:
            error_msg = f"Error calculating attendance: {str(e)}"
            print(error_msg)
            text_to_speech("Error occurred while calculating attendance")

    def display_attendance_window(df, subject_name, csv_file):
        """Display attendance in a scrollable window"""
        try:
            root = tkinter.Tk()
            root.title(f"Attendance Summary - {subject_name}")
            root.configure(background="black")
            root.geometry("900x600")

            # Create main frame
            main_frame = tk.Frame(root, bg="black")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Create canvas and scrollbar
            canvas = tk.Canvas(main_frame, bg="black")
            scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="black")

            # Configure scrolling
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Add title
            title_label = tk.Label(
                scrollable_frame,
                text=f"Attendance Summary - {subject_name}",
                font=("Arial", 16, "bold"),
                bg="black",
                fg="white",
                pady=10
            )
            title_label.grid(row=0, column=0, columnspan=len(df.columns), pady=10)

            # Display column headers
            for col_idx, column in enumerate(df.columns):
                header_label = tk.Label(
                    scrollable_frame,
                    text=str(column),
                    width=12,
                    height=2,
                    fg="yellow",
                    font=("times", 12, "bold"),
                    bg="black",
                    relief=tk.RIDGE,
                    bd=1
                )
                header_label.grid(row=1, column=col_idx, padx=1, pady=1, sticky="nsew")

            # Display data rows
            for row_idx, (_, row) in enumerate(df.iterrows(), start=2):
                for col_idx, value in enumerate(row):
                    # Color code attendance percentages
                    if col_idx == len(df.columns) - 1:  # Attendance column
                        try:
                            attendance_val = float(str(value).replace('%', ''))
                            if attendance_val >= 75:
                                fg_color = "green"
                            elif attendance_val >= 50:
                                fg_color = "yellow"
                            else:
                                fg_color = "red"
                        except:
                            fg_color = "white"
                    else:
                        fg_color = "white"

                    cell_label = tk.Label(
                        scrollable_frame,
                        text=str(value),
                        width=12,
                        height=2,
                        fg=fg_color,
                        font=("times", 10, "bold"),
                        bg="black",
                        relief=tk.RIDGE,
                        bd=1
                    )
                    cell_label.grid(row=row_idx, column=col_idx, padx=1, pady=1, sticky="nsew")

            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Add buttons frame
            button_frame = tk.Frame(root, bg="black")
            button_frame.pack(side="bottom", fill="x", padx=10, pady=5)

            # Export button
            def export_csv():
                text_to_speech("Attendance data exported successfully")
                print(f"Attendance data saved to: {csv_file}")

            export_btn = tk.Button(
                button_frame,
                text="Export CSV",
                command=export_csv,
                bg="green",
                fg="white",
                font=("times", 12, "bold"),
                width=12
            )
            export_btn.pack(side="left", padx=5)

            # Close button
            close_btn = tk.Button(
                button_frame,
                text="Close",
                command=root.destroy,
                bg="red",
                fg="white",
                font=("times", 12, "bold"),
                width=12
            )
            close_btn.pack(side="right", padx=5)

            # Mouse wheel scrolling
            def on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
            canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
            canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux

            root.mainloop()

        except Exception as e:
            print(f"Error displaying attendance window: {e}")

    # Create main subject selection window
    subject = Tk()
    subject.title("View Attendance")
    subject.geometry("600x350")
    subject.resizable(0, 0)
    subject.configure(background="black")

    # Title frame
    title_frame = tk.Frame(subject, bg="black", relief=RIDGE, bd=10)
    title_frame.pack(fill=X)

    titl = tk.Label(
        title_frame,
        text="View Attendance Summary",
        bg="black",
        fg="green",
        font=("arial", 24, "bold"),
        pady=10
    )
    titl.pack()

    # Input frame
    input_frame = tk.Frame(subject, bg="black")
    input_frame.pack(pady=30)

    sub_label = tk.Label(
        input_frame,
        text="Enter Subject:",
        bg="black",
        fg="yellow",
        font=("times new roman", 16, "bold")
    )
    sub_label.pack(pady=10)

    tx = tk.Entry(
        input_frame,
        width=20,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("times", 18, "bold"),
        justify='center'
    )
    tx.pack(pady=10)

    # Buttons frame
    button_frame = tk.Frame(subject, bg="black")
    button_frame.pack(pady=20)

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

        folder_path = os.path.join("Attendance", sub_clean)
        open_folder(folder_path)

    # Check Sheets button
    check_btn = tk.Button(
        button_frame,
        text="Open Folder",
        command=check_attendance_folder,
        bd=7,
        font=("times new roman", 14, "bold"),
        bg="#555555",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
        activebackground="#777777"
    )
    check_btn.pack(side="left", padx=10)

    # View Attendance button
    view_btn = tk.Button(
        button_frame,
        text="View Summary",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 14, "bold"),
        bg="#555555",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
        activebackground="#777777"
    )
    view_btn.pack(side="right", padx=10)

    # Instructions
    instruction_label = tk.Label(
        subject,
        text="Enter subject name and click 'View Summary' to see attendance statistics",
        bg="black",
        fg="gray",
        font=("arial", 10),
        pady=10
    )
    instruction_label.pack(side="bottom")

    # Center the window on screen
    subject.update_idletasks()
    x = (subject.winfo_screenwidth() // 2) - (subject.winfo_width() // 2)
    y = (subject.winfo_screenheight() // 2) - (subject.winfo_height() // 2)
    subject.geometry(f"+{x}+{y}")

    subject.mainloop()
