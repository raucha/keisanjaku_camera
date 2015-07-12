#!/usr/bin/env python
# coding=utf-8

import cv2
import numpy as np  # importing libraries
import math
import os
import sys

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
KEISANJAKU = '/keisanjaku.png'

# rawは(480,640,3)

th_bin = 1
cap = cv2.VideoCapture(0)  # creating camera object
hands_pos = [[0, 0],[0,0]]

while(cap.isOpened()):
    ret, raw = cap.read()  # reading the frames
    # gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    cv2.imshow('input', raw)
    img = cv2.GaussianBlur(raw, (15, 15), 0)

    fltr_min = np.array([150,120,10])
    fltr_max = np.array([180,255,200])
    # マスク画像を用いて元画像から指定した色を抽出
    im_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_fltr = cv2.inRange(im_hsv, fltr_min, fltr_max)
    diff = cv2.bitwise_and(img,img, mask=mask_fltr)
    diff = cv2.split(diff)[2]
    cv2.imshow('diff', diff)



    # img = raw

    # b = cv2.split(img)[0]
    # g = cv2.split(img)[1]
    # r = cv2.split(img)[2]
    # # cv2.imshow('b', b)
    # # cv2.imshow('g', g)
    # # cv2.imshow('r', r)
    # diff = cv2.add(-r, b)
    # diff = cv2.add(diff, g)
    # cv2.imshow('tmp', diff)
    gray = diff

    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    blur = gray
    # make binary image
    # ret, thresh1 = cv2.threshold(blur, th_bin, 255, cv2.THRESH_BINARY_INV)
    ret, thresh1 = cv2.threshold(blur, th_bin, 255, cv2.THRESH_BINARY)
    cv2.imshow('bin', thresh1)
    #モフォロジー演算
    # thresh1 = cv2.morphologyEx(
    #     thresh1, cv2.MORPH_OPEN, np.ones((15, 15), np.uint8))
    # thresh1 = cv2.morphologyEx(
    #     thresh1, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    thresh1 = cv2.morphologyEx(
        thresh1, cv2.MORPH_OPEN, np.ones((15, 15), np.uint8))
    thresh1 = cv2.morphologyEx(
        thresh1, cv2.MORPH_CLOSE, np.ones((50, 50), np.uint8))
    cv2.imshow('bin_mor', thresh1)

    #  輪郭抽出
    contours, _ = cv2.findContours(
        thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    hands = [None, None]
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

        # drawing = np.zeros(img.shape, np.uint8)
        # cv2.drawContours(drawing, hands, -1, (0, 255, 0), 2)  # contourIdx=0, thickness=2で描画
        # cv2.imshow('output', drawing)

        cv2.drawContours(raw, hands, -1, (255, 0, 0), 2)

        new_pos = [None, None]
        M = cv2.moments(hands[0])  # 輪郭点から白色1領域の重心を計算
        new_pos[0] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        M = cv2.moments(hands[1])
        new_pos[1] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # 向かって左側のを0番に
        if new_pos[1] < new_pos[0]:
            new_pos[0], new_pos[1] = new_pos[1], new_pos[0]
        hands_pos[0] = (int(0.8*hands_pos[0][0] + 0.2*new_pos[0][0]),int(0.8*hands_pos[0][1] + 0.2*new_pos[0][1]))
        hands_pos[1] = (int(0.8*hands_pos[1][0] + 0.2*new_pos[1][0]),int(0.8*hands_pos[1][1] + 0.2*new_pos[1][1]))
        # hands_pos[1][0] = int(0.8*hands_pos[1][0] + 0.2*new_pos[1][0])
        # hands_pos[1][1] = int(0.8*hands_pos[1][1] + 0.2*new_pos[1][1])
        # 重心を表示
        print(u"重心(" + str(hands_pos[0][0]) + "," + str(hands_pos[0][1]) + ")")
        cv2.circle(raw, hands_pos[0], 5, (0, 255, 0), -1)         # 重心を赤円で描く
        cv2.circle(raw, hands_pos[1], 5, (0, 255, 0), -1)
        jaku = cv2.imread(SCRIPT_PATH + KEISANJAKU)
        pos_diff = (
            hands_pos[1][0] - hands_pos[0][0], hands_pos[1][1] - hands_pos[0][1])
        # print hands_pos
        (space_y, space_x, ch) = raw[hands_pos[0][1]:hands_pos[0][1] + jaku.shape[0],
                                     hands_pos[0][0]:hands_pos[0][0] + jaku.shape[1]].shape
        print (space_y, space_x, ch), jaku.shape, jaku[:space_y, :space_x].shape
        print space_y, space_x
        raw[hands_pos[0][1]:hands_pos[0][1] + jaku.shape[0],
            hands_pos[0][0]:hands_pos[0][0] + jaku.shape[1]] = jaku[:space_y, :space_x]

    cv2.imshow('blur', blur)
    raw = cv2.resize(raw, (raw.shape[1] * 2, raw.shape[0] * 2))  # 画像を2倍に拡大
    cv2.imshow('add', raw)

    k = cv2.waitKey(10)
