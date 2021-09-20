import cv2 as cv
import numpy as np
def empty(a):
    pass

vid = cv.VideoCapture(1)

cv.namedWindow('cus')
cv.resizeWindow('cus',1000,500)
cv.createTrackbar('Hue_min','cus',58,179,empty)
cv.createTrackbar('Hue_max','cus',87,179,empty)
cv.createTrackbar('Sat_min','cus',33,255,empty)
cv.createTrackbar('Sat_max','cus',255,255,empty)
cv.createTrackbar('Val_min','cus',49,255,empty)
cv.createTrackbar('Val_max','cus',255,255,empty)

g_p = []
r_p = []
y_p = []
b_p = []
c_name = 'r'
while True:

    s,img = vid.read()
    img_c = img.copy()
    img_hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)


    cv.rectangle(img,(0,0),(100,100),(0,0,0),-1)
    cv.putText(img,'Clear ALl',(20,60),cv.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
    cv.rectangle(img, (100, 0), (200, 100), (0, 0, 255), -1)
    cv.putText(img, 'Red', (130, 60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv.rectangle(img, (200, 0), (300, 100), (255, 0, 0), -1)
    cv.putText(img, 'Blue', (230, 60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv.rectangle(img, (300, 0), (400, 100), (0, 255, 255), -1)
    cv.putText(img, 'Yellow', (330, 60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0,0), 1)
    cv.rectangle(img, (400, 0), (500, 100), (0, 255, 0), -1)
    cv.putText(img, 'Green', (430, 60), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)


    hm = cv.getTrackbarPos('Hue_min', 'cus')
    hma = cv.getTrackbarPos('Hue_max', 'cus')
    sm = cv.getTrackbarPos('Sat_min', 'cus')
    sma = cv.getTrackbarPos('Sat_max', 'cus')
    vm = cv.getTrackbarPos('Val_min', 'cus')
    vma = cv.getTrackbarPos('Val_max', 'cus')

    l = np.array([hm,sm,vm])
    h = np.array([hma,sma,vma])
    mask = cv.inRange(img_hsv,l,h)


    countor,h = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img_c,countor,-1,(0,255,0),3)

    cv.imshow('mask', cv.bitwise_and(img,img,mask = mask))
    cv.imshow('counters', img_c)



    for c in countor:

        if cv.contourArea(c) > 100:

            ((x,y),r) = cv.minEnclosingCircle(c)
            c_x = int(x)
            c_y = int(y)
            cv.circle(img,(int(c_x),int(c_y)),int(r),(0,255,0),1)
            cv.circle(img, (int(c_x), int(c_y)), 5, (0, 255, 0), -1)

            if c_x < 100 and c_x > 0 and c_y < 100 and c_y > 0:
                g_p.clear()
                r_p.clear()
                b_p.clear()
                y_p.clear()
            if c_x > 100 and c_x < 200 and c_y < 100 and c_y > 0:
                colour = (0,0,255)
                c_name = 'r'
            elif c_x > 200 and c_x < 300 and c_y < 100 and c_y > 0:
                colour = (255, 0, 0)
                c_name = 'b'
            elif c_x > 300 and c_x < 400 and c_y < 100 and c_y > 0:
                colour = (0, 255, 255)
                c_name = 'y'
            elif c_x > 400 and c_x < 500 and c_y < 100 and c_y > 0:
                colour = (0, 255, 0)
                c_name = 'g'

            else:
                if c_name == 'r':
                    r_p.append((c_x, c_y))
                elif c_name == 'b':
                    b_p.append((c_x, c_y))
                elif c_name == 'g':
                    g_p.append((c_x, c_y))
                elif c_name == 'y':
                    y_p.append((c_x, c_y))

    for point in g_p:
        cv.circle(img, point, 5, (0, 255, 0), -1)
    for point in r_p:
        cv.circle(img, point, 5, (0, 0, 255), -1)
    for point in b_p:
        cv.circle(img, point, 5, (255, 0, 0), -1)
    for point in y_p:
        cv.circle(img, point, 5, (0, 255, 255), -1)






    cv.imshow('paint',img)


    if cv.waitKey(1) & 0xFF == 27:
        break