import cv2
import numpy as np  # importing libraries


cap = cv2.VideoCapture(0)  # creating camera object
th_bin = int(raw_input("maek bin image threshold: "))
while(cap.isOpened()):
    ret, img = cap.read()  # reading the frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    b = cv2.split(img)[0]
    cv2.imshow('b', b)
    g = cv2.split(img)[1]
    cv2.imshow('g', g)
    r = cv2.split(img)[2]
    cv2.imshow('r', r)
    # gray = (r-b)-g
    # test = r-b
    # cv2.imshow('test', test)
    # print type(gray)
    # diff = r
    # diff = cv2.Sub(r,b,r)
    diff = cv2.add(r,-b)
    cv2.imshow('diff', diff)
    diff2 = cv2.add(-r,b)
    cv2.imshow('diff2', diff2)
    tmp = cv2.add(-r,b)
    tmp = cv2.add(tmp,g)
    cv2.imshow('tmp', tmp)
    tmp2 = cv2.add(-b,g)
    tmp2 = cv2.add(tmp,r)
    cv2.imshow('tmp2', tmp2)
    # print diff


    # print len(img)
    # cv2.imshow('input', img)  # displaying the frames
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # ret, thresh1 = cv2.threshold(
    #     blur, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    ret, thresh1 = cv2.threshold(
        blur, th_bin, 255, cv2.THRESH_BINARY)
    cv2.imshow('bin', thresh1)
    # thresh1_orig = thresh1

    contours, hierarchy = cv2.findContours(
        thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# >extract the largest contour
    max_area = 1
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

    cv2.imshow('input', img)
    cv2.imshow('blur', blur)
    # cv2.imshow('bin', thresh1_orig)
    # cv2.imshow('hull', hull)
    cv2.imshow('output', drawing)
    k = cv2.waitKey(10)
    # print "ret:", ret, "    k", k
    if k == 27:
        break
