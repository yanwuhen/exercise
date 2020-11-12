import cv2
import time

MAX_THRESHOLD = 3   #多少帧变化才录像
MAX_DELTA_SUM = 300 #多大变化才算
WIDTH = 640
HEIGHT = 480
FPS = 20

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("test_data_360.mp4")
if not cap.isOpened():
    print("dont open")
    exit
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(cv2.CAP_PROP_FPS, FPS)
fourcc = cv2.VideoWriter_fourcc(*'AVC1')
out = None

intrusion_threshold = MAX_THRESHOLD
i = last_change = 0
bgray = None
while True:
    i += 1
    ret, nframe = cap.read()
    if not ret:
        print("cant read at %d frame" % i)
        break
    ngray = cv2.cvtColor(nframe, cv2.COLOR_BGR2GRAY)
    cv2.GaussianBlur(ngray, (21, 21), 0)
    if i == 1:
        bgray = ngray
        continue
    frameDelta = cv2.absdiff(cv2.convertScaleAbs(
        ngray), cv2.convertScaleAbs(bgray.copy()))
    bgray = ngray
    thresh = cv2.threshold(frameDelta, 45, 255, cv2.THRESH_BINARY)[1]
    if thresh.sum() > MAX_DELTA_SUM:
        print(i, thresh.sum())
        #cv2.imwrite("/mnt/jk/%d_new.jpg" % i, ngray)
        if i == last_change + 1:
            intrusion_threshold -= 1
        last_change = i
    if intrusion_threshold < 0 and out is None:
        out = cv2.VideoWriter('/mnt/jk/save-%s.avi' % time.strftime('%y-%m-%d-%H-%M-%S'), fourcc, FPS, (WIDTH, HEIGHT))
    if last_change != i:
        intrusion_threshold = MAX_THRESHOLD
        if out is not None:
            out.release()
            out = None
    if out is not None:
        out.write(nframe)
cap.release()
