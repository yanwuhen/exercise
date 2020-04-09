import cv2
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("test_data_360.mp4")
if not cap.isOpened():
    print("dont open")
    exit
# max_cap = 1000
i = 0
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
    # if i == 450:
    #     cv2.imwrite("0409_%d_delta.jpg" % i, frameDelta)
    #     cv2.imwrite("0409_%d_old.jpg" % i, bgray)
    #     cv2.imwrite("0409_%d_new.jpg" % i, ngray)
    if thresh.sum() > 300:
        print(i, thresh.sum())
        cv2.imwrite("jk/%d_new.jpg" % i, ngray)
        # max_cap -= 1
        # if max_cap <= 0:
        #     break
cap.release()
