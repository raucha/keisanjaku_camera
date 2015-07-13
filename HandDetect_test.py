#!/usr/bin/env python
# coding=utf-8

import cv2
import numpy as np  # importing libraries
import math
import os
import sys

# rawは(480,640,3)
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
KEISANJAKU = '/keisanjaku.png'
KEISANJAKU2 = '/keisanjaku2.png'
cap = cv2.VideoCapture(0)  # creating camera object
hands_pos = [[0, 0], [0, 0]]

while(cap.isOpened()):
    ret, raw = cap.read()  # reading the frames
    # gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    cv2.imshow('input', raw)
    # img = cv2.GaussianBlur(raw, (15, 15), 0)
    # masked = raw

    # fltr_min = np.array([150, 120, 10])
    # fltr_max = np.array([180, 255, 200])
    fltr_min = np.array([150, 100, 100])
    fltr_max = np.array([180, 255, 255])
    # マスク画像を用いて元画像から指定した色を抽出
    im_hsv = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)
    mask_fltr = cv2.inRange(im_hsv, fltr_min, fltr_max)
    fltr_min = np.array([0, 180, 120])
    fltr_max = np.array([5, 255, 255])
    # マスク画像を用いて元画像から指定した色を抽出
    im_hsv = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)
    mask_fltr += cv2.inRange(im_hsv, fltr_min, fltr_max)

    cv2.imshow('mask', mask_fltr)
    masked = cv2.bitwise_and(raw, raw, mask=mask_fltr)

    # cv2.imshow('bef', masked)
    masked = cv2.split(masked)[2]  # 赤だけ取り出す
    cv2.imshow('masked', masked)

    # 2値化
    _ret, bined = cv2.threshold(masked, 1, 255, cv2.THRESH_BINARY)
    cv2.imshow('bined', bined)

    # モフォロジー演算
    morphed = bined
    # morphed = masked
    morphed = cv2.morphologyEx(
        morphed, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    cv2.imshow('morph_close', morphed)
    morphed = cv2.morphologyEx(
        morphed, cv2.MORPH_OPEN, np.ones((15, 15), np.uint8))
    cv2.imshow('morph_close_opne', morphed)

    #  輪郭抽出
    contours, _ = cv2.findContours(
        morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hands = [None, None]
    resized = cv2.resize(raw, (raw.shape[1] * 2, raw.shape[0] * 2))  # 画像を2倍に拡大
    if 2 <= len(contours):
        maxs = [0, 0]
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

        cv2.drawContours(raw, hands, -1, (255, 0, 0), 2)

        new_pos = [None, None]
        M = cv2.moments(hands[0])  # 輪郭点から白色1領域の重心を計算
        new_pos[0] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        M = cv2.moments(hands[1])
        new_pos[1] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # 向かって左側のを0番に
        if new_pos[1] < new_pos[0]:
            new_pos[0], new_pos[1] = new_pos[1], new_pos[0]
        hands_pos[0] = (int(0.8 * hands_pos[0][0] + 0.2 * new_pos[0][0]),
                        int(0.8 * hands_pos[0][1] + 0.2 * new_pos[0][1]))
        hands_pos[1] = (int(0.8 * hands_pos[1][0] + 0.2 * new_pos[1][0]),
                        int(0.8 * hands_pos[1][1] + 0.2 * new_pos[1][1]))
        # 重心を表示
        # print(u"重心(" + str(hands_pos[0][0]) + "," + str(hands_pos[0][1]) + ")")
        cv2.circle(raw, hands_pos[0], 5, (0, 255, 0), -1)         # 重心を赤円で描く
        cv2.circle(raw, hands_pos[1], 5, (0, 255, 0), -1)
        # print hands_pos

        # 画像を2倍に拡大
        resized = cv2.resize(raw, (raw.shape[1] * 2, raw.shape[0] * 2))

    jaku = cv2.imread(SCRIPT_PATH + KEISANJAKU)
    jaku2 = cv2.imread(SCRIPT_PATH + KEISANJAKU2)
    # 計算尺を表示
    jaku_pos = (2*hands_pos[0][0], 2*hands_pos[0][1])
    (space_y, space_x, ch) = resized[jaku_pos[1]:jaku_pos[1] + jaku.shape[0],
                                     jaku_pos[0]:jaku_pos[0] + jaku.shape[1]].shape
    # print (space_y, space_x, ch), jaku.shape, jaku[:space_y, :space_x].shape
    resized[jaku_pos[1]:jaku_pos[1] + jaku.shape[0],
            jaku_pos[0]:jaku_pos[0] + jaku.shape[1]] = jaku[:space_y, :space_x]

    # 計算尺2を表示
    jaku2_pos = (2*hands_pos[1][0], 2*hands_pos[0][1] + jaku.shape[0])
    (space_y, space_x, ch) = resized[jaku2_pos[1]:jaku2_pos[1] + jaku2.shape[0],
                                     jaku2_pos[0]:jaku2_pos[0] + jaku2.shape[1]].shape
    # print (space_y, space_x, ch), jaku.shape, jaku[:space_y, :space_x].shape
    resized[jaku2_pos[1]:jaku2_pos[1] + jaku2.shape[0],
            jaku2_pos[0]:jaku2_pos[0] + jaku2.shape[1]] = jaku2[:space_y, :space_x]

    cv2.imshow('add', resized)
    k = cv2.waitKey(10)
