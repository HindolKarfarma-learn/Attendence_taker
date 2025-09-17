import os
import cv2
import numpy as np
from PIL import Image

def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)

    faces, Ids = getImagesAndLabels(trainimage_path)

    recognizer.train(faces, np.array(Ids))
    recognizer.save(trainimagelabel_path)

    res = "Image trained successfully"
    message.configure(text=res)
    text_to_speech(res)


def getImagesAndLabels(path):
    faces = []
    Ids = []

    # Go through each student folder
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)

        if not os.path.isdir(folder_path):
            continue  # skip if not a directory

        # folder format is Enrollment_Name
        try:
            enrollment_id = int(folder.split("_")[0])
        except ValueError:
            print(f"Skipping folder {folder}: invalid enrollment format")
            continue

        # Iterate through all image files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Only process valid image files
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            try:
                pilImage = Image.open(file_path).convert("L")
            except Exception as e:
                print(f"Skipping file {file_path}: {e}")
                continue

            imageNp = np.array(pilImage, "uint8")
            faces.append(imageNp)
            Ids.append(enrollment_id)

    return faces, Ids
