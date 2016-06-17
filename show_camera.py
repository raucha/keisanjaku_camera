# -*- coding: utf-8 -*-
import cv2
import os
import sys


cap = cv2.VideoCapture(0)  # creating camera object

def main():
    while(cap.isOpened()):
        ret, im = cap.read()  # reading the frames
        # 結果を表示
        cv2.imshow("Show Image",im)
        k = cv2.waitKey(10)
    # cv2.waitKey(0)              # キー入力待機
    # cv2.destroyAllWindows()     # ウィンドウ破棄

if __name__ == '__main__':
   main()
