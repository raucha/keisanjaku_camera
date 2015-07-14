# -*- coding: utf-8 -*-
import cv2
import os
import sys

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
FACE_XML = '/haarcascade_frontalface_default.xml'

cap = cv2.VideoCapture(0)  # creating camera object

def main():
   # 画像の読み込み
    while(cap.isOpened()):
        ret, im = cap.read()  # reading the frames
        # im = cv2.imread("test.png")
        cascade = cv2.CascadeClassifier(SCRIPT_PATH+FACE_XML)    # 分類器をロード
        face = cascade.detectMultiScale(im, 1.1, 3)    # 顔探索(画像,縮小スケール,最低矩形数)
        # 顔検出した部分にモザイク処理
        for (x, y, w, h) in face:
            im2 = im[y:y+h, x:x+w]
            im2 = cv2.resize(im2, (w/10, h/10))
            im2 = cv2.resize(im2, (w, h), interpolation=cv2.cv.CV_INTER_NN)
            im[y:y+h, x:x+w] = im2

        # 結果を表示
        cv2.imshow("Show Image",im)
        k = cv2.waitKey(10)
    # cv2.waitKey(0)              # キー入力待機
    # cv2.destroyAllWindows()     # ウィンドウ破棄

if __name__ == '__main__':
   main()
