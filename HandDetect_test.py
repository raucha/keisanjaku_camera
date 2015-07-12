import cv2
import numpy as np  # importing libraries


cap = cv2.VideoCapture(0)  # creating camera object
# th_bin = int(raw_input("maek bin image threshold: "))
th_bin = 254
while(cap.isOpened()):
    ret, raw = cap.read()  # reading the frames
    # gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    cv2.imshow('input', raw)
    img = cv2.GaussianBlur(raw, (25,25), 0)

    b = cv2.split(img)[0]
    g = cv2.split(img)[1]
    r = cv2.split(img)[2]
    # cv2.imshow('b', b)
    # cv2.imshow('g', g)
    # cv2.imshow('r', r)
    diff = cv2.add(-r, b)
    diff = cv2.add(diff, g)
    cv2.imshow('tmp', diff)
    gray = diff

    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    blur = gray
    # make binary image
    ret, thresh1 = cv2.threshold(
        blur, th_bin, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('bin', thresh1)
    thresh1=cv2.morphologyEx(thresh1,cv2.MORPH_OPEN,np.ones(15,15),np.uint8))
    cv2.imshow('bin_mor', thresh1)
    # thresh1_orig = thresh1

    contours, hierarchy = cv2.findContours(
        thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# >extract the largest contour

    if 0 != len(contours):
        max_area = 1
        if 0 == len(contours):
            continue
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if(area > max_area):
                max_area = area
                ci = i
        cnt = contours[ci]
    # >now draw the convex hull
        hull = cv2.convexHull(cnt)
    # >displaying largest contour and convex hull
        drawing = np.zeros(img.shape, np.uint8)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 2)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 2)
        cv2.imshow('output', drawing)

    cv2.imshow('blur', blur)
    # cv2.imshow('bin', thresh1_orig)
    # cv2.imshow('hull', hull)
    k = cv2.waitKey(10)
    # print "ret:", ret, "    k", k
    if k == 27:
        break
