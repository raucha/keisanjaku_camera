#!/usr/bin/env python
# coding=utf-8

import cv2
import numpy as np  # importing libraries
import math
import os, sys

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
KEISANJAKU = 'keisanjaku.png'

# rawは(480,640,3)

cap = cv2.VideoCapture(0)  # creating camera object
# th_bin = int(raw_input("maek bin image threshold: "))
th_bin = 254
while(cap.isOpened()):
    ret, raw = cap.read()  # reading the frames
    # gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    cv2.imshow('input', raw)
    img = cv2.GaussianBlur(raw, (15, 15), 0)
    # img = raw

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
    thresh1 = cv2.morphologyEx(
        thresh1, cv2.MORPH_OPEN, np.ones((15, 15), np.uint8))
    thresh1 = cv2.morphologyEx(
        thresh1, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    cv2.imshow('bin_mor', thresh1)

    contours, hierarchy = cv2.findContours(
        thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #>extract the largest contour
    # print len(contours) #lenは塊の個数を変えす
    # if 0 != len(contours):
    #     max_area = 0
    #     for i in range(len(contours)):
    #         cnt = contours[i]
    #         area = cv2.contourArea(cnt)  # 外形が囲む面積を求める
    #         if(area > max_area):
    #             max_area = area
    #             ci = i
    #     cnt = contours[ci]  # 面積最大の輪郭線だけ利用
    #
    #     hull = cv2.convexHull(cnt)  # 凸集合の頂点集合
    #
    #     drawing = np.zeros(img.shape, np.uint8)
    #     # contourIdx=0, thickness=2で描画
    #     cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 2)
    #     cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 2)
    #     # cv2.drawcontours(image, contours, contourIdx, color, thickness=None, lineType=None, hierarchy=None, maxLevel=None, offset=None)
    #     cv2.imshow('output', drawing)

    hands = [None, None]
    hands_pos = [None, None]
    if 2 <= len(contours):
        maxs = [int(0), int(0)]
        # max_area = 0
        for i in range(len(contours)):
            cnt = contours[i]
            cnt_size = cv2.contourArea(cnt)
            if cnt_size > maxs[0]:
                maxs[1] = maxs[0]
                maxs[0] = cnt_size
                hands[1] = hands[0]
                hands[0] = cnt
            elif cnt_size > maxs[1]:
                maxs[1] = cnt_size
                hands[1] = cnt

        # hull = cv2.convexHull(cnt)  # 凸集合の頂点集合

        # drawing = np.zeros(img.shape, np.uint8)
        # cv2.drawContours(drawing, hands, -1, (0, 255, 0), 2)  # contourIdx=0, thickness=2で描画
        # cv2.imshow('output', drawing)

        cv2.drawContours(raw, hands, -1, (255, 0, 0), 2)

        M = cv2.moments(hands[0])  # 輪郭点から白色1領域の重心を計算
        # (cx, cy) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        hands_pos[0] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        M = cv2.moments(hands[1])  # 輪郭点から白色領域の重心を計算
        hands_pos[1] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # 向かって左側のを0番に
        if hands_pos[1] < hands_pos[0]:
            hands_pos[0], hands_pos[1] = hands_pos[1], hands_pos[0]
        # 重心を表示
        print(u"重心(" + str(hands_pos[0][0]) + "," + str(hands_pos[0][1]) + ")")
        cv2.circle(raw, hands_pos[0], 5, (0, 255, 0), -1)         # 重心を赤円で描く
        cv2.circle(raw, hands_pos[1], 5, (0, 255, 0), -1)         # 重心を赤円で描く
        jaku = cv2.imread(SCRIPT_PATH+KEISANJAKU)
        # cv2.imshow('jaku', jaku)
        pos_diff = (hands_pos[1][0]-hands_pos[0][0], hands_pos[1][1]-hands_pos[0][1])
        # print hands_pos
        # print raw[hands_pos[0][1]:hands_pos[0][1] + jaku.shape[1], hands_pos[0][0]:hands_pos[0][0] + jaku.shape[0]].shape
        (space_x, space_y, ch) = raw[hands_pos[0][1]:hands_pos[0][1] + jaku.shape[1], hands_pos[0][0]:hands_pos[0][0] + jaku.shape[0]].shape
        raw[hands_pos[0][1]:hands_pos[0][1] + jaku.shape[1], hands_pos[0]
            [0]:hands_pos[0][0] + jaku.shape[0]] = jaku[:space_x, :space_y]

    cv2.imshow('blur', blur)

    cv2.imshow('add', raw)

    k = cv2.waitKey(10)
    # print "ret:", ret, "    k", k
    if k == 27:
        break
