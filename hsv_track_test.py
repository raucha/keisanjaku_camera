# -*- coding: utf-8 -*-
import cv2
import numpy as np

if __name__ == '__main__':

    # カメラ映像の取得
    cap = cv2.VideoCapture(0)

    while True:
        ret, im = cap.read()
        im_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        cv2.imshow("CV2 Camera",im)
        # 緑色(HSV)の範囲を定義
        # green_min = np.array([40,10,0])
        # green_max = np.array([70,255,255])
        # fltr_min = np.array([95,50,20])        # 青
        # fltr_max = np.array([125,255,255])
        fltr_min = np.array([160,120,10])
        fltr_max = np.array([180,255,200])
        # マスク画像を用いて元画像から指定した色を抽出
        mask_fltr = cv2.inRange(im_hsv, fltr_min, fltr_max)
        im_fltr = cv2.bitwise_and(im,im, mask=mask_fltr)
        cv2.imshow("CV2 Camera2",im_fltr)
        # キーが押されたらループから抜ける
        if cv2.waitKey(10) > 0:
            break

    # キャプチャー解放
    cap.release()
    # ウィンドウ破棄
    cv2.destroyAllWindows()
