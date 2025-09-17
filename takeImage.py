# import csv
# import os, cv2
# import numpy as np
# import pandas as pd
# import datetime
# import time



# # take Image of user
# def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen,text_to_speech):
#     if (l1 == "") and (l2==""):
#         t='Please Enter the your Enrollment Number and Name.'
#         text_to_speech(t)
#     elif l1=='':
#         t='Please Enter the your Enrollment Number.'
#         text_to_speech(t)
#     elif l2 == "":
#         t='Please Enter the your Name.'
#         text_to_speech(t)
#     else:
#         try:
#             cam = cv2.VideoCapture(0)
#             detector = cv2.CascadeClassifier(haarcasecade_path)
#             Enrollment = l1
#             Name = l2
#             sampleNum = 0
#             directory = Enrollment + "_" + Name
#             path = os.path.join(trainimage_path, directory)
#             os.mkdir(path)
#             while True:
#                 ret, img = cam.read()
#                 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#                 faces = detector.detectMultiScale(gray, 1.3, 5)
#                 for (x, y, w, h) in faces:
#                     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#                     sampleNum = sampleNum + 1
#                     cv2.imwrite(
#                         f"{path}\ "
#                         + Name
#                         + "_"
#                         + Enrollment
#                         + "_"
#                         + str(sampleNum)
#                         + ".jpg",
#                         gray[y : y + h, x : x + w],
#                     )
#                     cv2.imshow("Frame", img)
#                 if cv2.waitKey(1) & 0xFF == ord("q"):
#                     break
#                 elif sampleNum > 50:
#                     break
#             cam.release()
#             cv2.destroyAllWindows()
#             row = [Enrollment, Name]
#             with open(
#                 "StudentDetails/studentdetails.csv",
#                 "a+",
#             ) as csvFile:
#                 writer = csv.writer(csvFile, delimiter=",")
#                 writer.writerow(row)
#                 csvFile.close()
#             res = "Images Saved for ER No:" + Enrollment + " Name:" + Name
#             message.configure(text=res)
#             text_to_speech(res)
#         except FileExistsError as F:
#             F = "Student Data already exists"
#             text_to_speech(F)
import csv
import os
import cv2

def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    # Basic input validation
    if (l1.strip() == "") and (l2.strip() == ""):
        text_to_speech('Please enter your Enrollment Number and Name.')
        return
    elif l1.strip() == '':
        text_to_speech('Please enter your Enrollment Number.')
        return
    elif l2.strip() == "":
        text_to_speech('Please enter your Name.')
        return

    try:
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(haarcasecade_path)

        Enrollment = l1.strip()
        # Make name filesystem-safe (no spaces or special characters)
        Name = l2.strip().replace(" ", "_")

        sampleNum = 0

        # Create directory: TrainingImage/Enrollment_Name
        student_dir = os.path.join(trainimage_path, f"{Enrollment}_{Name}")
        os.makedirs(student_dir, exist_ok=True)

        while True:
            ret, img = cam.read()
            if not ret:
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1

                # Build a cross-platform file path
                img_filename = f"{Enrollment}_{Name}_{sampleNum}.jpg"
                img_path = os.path.join(student_dir, img_filename)

                cv2.imwrite(img_path, gray[y:y + h, x:x + w])
                cv2.imshow("Frame", img)

            # Press 'q' to quit or stop after 50 samples
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            elif sampleNum >= 50:
                break

        cam.release()
        cv2.destroyAllWindows()

        # Append to CSV (newline="" fixes Windows extra blank lines issue)
        os.makedirs("StudentDetails", exist_ok=True)
        with open("StudentDetails/studentdetails.csv", "a+", newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([Enrollment, Name])

        res = f"Images saved for ER No: {Enrollment}  Name: {Name}"
        message.configure(text=res)
        text_to_speech(res)

    except Exception as e:
        text_to_speech("Error occurred while capturing images.")
        print("Error:", e)
