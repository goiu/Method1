# -*- coding: utf-8 -*-
"""
Created on Thu May 25 02:07:14 2020
CSE 30 Spring 2020 Program 4 starter code
@author: Fahim
"""

import cv2
import numpy as np

cap = cv2.VideoCapture('sample.webm')
#cap = cv2.VideoCapture(0)
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)
while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)

        if w * h > 9000:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        elif w*h > 5250:
            rec = cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)
            rec
            cv2.putText(rec, 'Contaminated', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (36, 255, 12), 2)

    """ 
    if cv2.contourArea(contour) > 900 and cv2.contourArea(contour) < 1000:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        elif cv2.contourArea(contour) > 3500:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)
    """
        #if cv2.boundingRect(contour) > 100:
         #   cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)

    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    image = cv2.resize(frame1, (640,480))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()