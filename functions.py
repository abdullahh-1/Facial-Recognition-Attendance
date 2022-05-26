import copy
import cv2
import numpy
import os
from os import listdir
from os.path import isfile, join


def search_name(name, sheet):
    for row in sheet:
        l_name, c, l_date = row.partition(',')
        if l_name == name:
            return True
    return False


def digital_attendance():
    mypath = 'picture_database'
    only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    only_files.pop(0)
    cascPath = 'cascade.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)
    video_capture = cv2.VideoCapture(0)
    student_names = []

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):

            img = copy.deepcopy(gray)  # Path of an image
            faceCascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
            faces = faceCascade.detectMultiScale(img, 1.1, 4)

            directory = os.getcwd() + r''
            try:
                if not os.path.exists(directory):
                    os.mkdir(directory)
            except FileExistsError as fee:
                print('Exception Occured', fee)
            os.chdir(directory)
            i = 1
            for (x, y, w, h) in faces:
                FaceImg = img[y:y + h, x:x + w]

                # To save an image on disk
                filename = 'Face' + str(i) + '.jpg'
                cv2.imwrite(filename, FaceImg)
                i += 1

                for pic in only_files:
                    pic = "picture_database/" + pic
                    template = cv2.imread(pic, 0)

                    w, h = template.shape[::-1]
                    res = cv2.matchTemplate(FaceImg, template, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.7

                    loc = numpy.where(res >= threshold)
                    if len(loc[0]) > 0:
                        student_name = pic[:-5]
                        student_name = student_name[17:]
                        student_names.append(student_name)
                        print(filename, student_name)

                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(gray, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                    cv2.imwrite('res.png', gray)
                    cv2.imshow('Video', gray)
                    video_capture.release()
                    cv2.destroyAllWindows()

            return student_names
