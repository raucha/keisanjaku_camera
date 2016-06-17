# -*- coding: utf-8 -*-
import cv2
import numpy as np

(cx, cy) = (0, 0)           # クリックされた座標


def nothing(x):
    pass

# マウスクリックの処理


def onMouse(event, x, y, flags, param):
    global cx, cy, click_r
    if event == cv2.EVENT_MOUSEMOVE:
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        (cx, cy) = (x, y)
        return

# カラートラッキング


def color_track(im, x, y, hw, sw, vw):
    k = np.ones((5, 5), np.uint8)  # 膨張化用のカーネル
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)  # RGB色空間からHSV色空間に変換
    h, s, v = hsv[y, x]        # HSVを抽出
    print "{0:>3} {1:>3} {2:>3}".format(h, s, v)
    hsv_min = np.array([h - hw, s - sw, v - vw])
    hsv_max = np.array([h + hw, s + sw, v + vw])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)      # マスク画像の生成
    mask2 = cv2.dilate(mask2, k, iterations=2)    # 膨張化
    mask2 = cv2.erode(mask2, k, iterations=2)    # 膨張化
    return mask2

# 要素数が最大のインデックス


def index_emax(cnt, nmax=0, imax=-1):
    for i in range(len(cnt)):
        ncnt = len(cnt[i])
        if ncnt > nmax:
            nmax = ncnt
            imax = i

    return imax


def main():
    (x, y) = (200, 200)
    cap = cv2.VideoCapture(0)
    ret, im = cap.read()
    # トラックバーの作成
    cv2.namedWindow("Viewer")
    cv2.createTrackbar("H", "Viewer", 0, 127, nothing)
    cv2.createTrackbar("S", "Viewer", 0, 127, nothing)
    cv2.createTrackbar("V", "Viewer", 0, 127, nothing)
    while(1):
        ret, im = cap.read()
        # 計算高速化のために画像サイズを1/2
        #im = cv2.resize(im,(im.shape[1]/2,im.shape[0]/2))
        hw = cv2.getTrackbarPos("H", "Viewer")   # Hの上下限幅を取得
        sw = cv2.getTrackbarPos("S", "Viewer")   # Sの上下限幅を取得
        vw = cv2.getTrackbarPos("V", "Viewer")   # Vの上下限幅を取得
        cv2.setMouseCallback("Viewer", onMouse)                # マウスイベント
        # 左クリックされた場合
        if(cx != 0):
            (x, y) = (cx, cy)
        mask = color_track(im, x, y, hw, sw, vw)
        cnt = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        n = index_emax(cnt)
        if n != -1:
            hull = cv2.convexHull(cnt[n])
            # cv2.drawContours(im, [hull], -1, (0, 200, 0), 3)
            cv2.drawContours(im, cnt, -1, (0, 200, 0), 3)

        # 結果表示
        cv2.rectangle(im, (cx - 5, cy - 5), (cx + 5, cy + 5), (0, 50, 255), 2)
        cv2.imshow("Viewer", im)
        # 任意のキーが押されたら終了
        if cv2.waitKey(10) > 0:
            cap.release()
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
