import cv2
import numpy
from os import listdir
from os.path import isfile, join
from csv import writer
import datetime

if __name__ == '__main__':
    mypath = 'picture_database'
    only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    only_files.pop(0)
    cascPath = 'cascade.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)

    video_capture = cv2.VideoCapture(0)

    student_name = " "

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(30, 30))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            for pic in only_files:
                pic = "picture_database/" + pic
                template = cv2.imread(pic, 0)

                w, h = template.shape[::-1]
                res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.7

                loc = numpy.where(res >= threshold)
                if len(loc[0]) > 0:
                    student_name = pic[:-4]
                    student_name = student_name[17:]
                    print(student_name)

                for pt in zip(*loc[::-1]):
                    cv2.rectangle(gray, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                cv2.imwrite('res.png', gray)
                cv2.imshow('Video', gray)
                video_capture.release()
                cv2.destroyAllWindows()

            break

    if student_name != " ":
        new_entry = [student_name, datetime.datetime.now()]
        with open('attendance.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(new_entry)
            f_object.close()
