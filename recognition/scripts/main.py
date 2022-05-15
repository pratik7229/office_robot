# File Import
from face_detection import face_rec
import functions


if __name__ == "__main__":
    if functions.checkInternetConnection() == True:
        obj = face_rec()    # creating an object for the class face_rec
        obj.face_detect() # Calling face_detect function from face_rec call. It is the main function from where the execution starts
                            




