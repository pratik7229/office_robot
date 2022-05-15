#!/usr/bin/env python3

# File import
# from functions import wishMe


# Libraries
import cv2
import numpy as np
import face_recognition
import os


class face_rec:
    
    def __init__(self):                 #Constructor
        self.path = '/home/pratik/office_rbt_ws/src/recognition/scripts/Training_images'
        self.images = []
        self.classNames = []
        myList = os.listdir(self.path)
        print(myList)
        for cl in myList:
            p = os.path.join(self.path, cl)
            curImg = cv2.imread(p)
            self.images.append(curImg)
            self.classNames.append(os.path.splitext(cl)[0])
        self.encodeListKnown = self.findEncodings(self.images)

    def findEncodings(self,images):
        """
        This fucntion compares the input image with the stored images
        
        """

        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    def face_detect(self):
        """
        This function detects the face using camera
        
        """


        print('Encoding Complete')

        self.cap = cv2.VideoCapture(0) #camera is switched on
        counter = 0                    # counter variable to make the program run only once 
        while counter<1:
            success, img = self.cap.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(self.encodeListKnown, encodeFace)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = self.classNames[matchIndex].upper()
                    # cv2.imshow('Webcam', img)
                    # cv2.waitKey(1)
                    # print(name)
                    name = name.lower()
                    # wishMe(name)        # wishMe functions from the functions.py file is called with name as its parameter
                    counter += 1
                    self.cap.release()
        return name

                    
