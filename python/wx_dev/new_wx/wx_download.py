# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import werobot
import threading
import time
import json
import cv2

g_pic_user = None
g_user_config = {}

robot = werobot.WeRoBot(token='Lucy2017')

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
# 测试微信号
robot.config["APP_ID"] = "wx204ef573e97fe056"
robot.config["APP_SECRET"] = "6601eb26017705c8343eeb7a9c5bcaf6"
# robot.config["APP_ID"] = "wxf90ffdab74eb6c6c"
# robot.config["APP_SECRET"] = "83b5fe9743c4e68ee423083d7978ebdf"
# robot.config["ENCODING_AES_KEY"] = "EwECOhBNuQBpllQvCko8KBhge61Mug2ibimC5g5r8dC"
client = robot.client


def thread_wait_send():
    global g_pic_user
    while True:
        if g_pic_user:
            # os.system("raspistill -w 640 -h 360 -o %s.jpg" % user_id)
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if not ret:
                print("ret = %s" % ret)
                return
            cv2.imwrite("%s.jpg" % g_pic_user, frame)
            with open("%s.jpg" % g_pic_user, "rb") as pic_file:
                ret = client.upload_permanent_media(
                    media_type="image", media_file=pic_file)
                print(type(ret), ret)
                j = eval(str(ret))
            media_id = j['media_id']
            client.send_image_message(user_id=g_pic_user, media_id=media_id)
            g_pic_user = None
        time.sleep(1)


t = threading.Thread(target=thread_wait_send)
t.start()


@robot.filter('jk')
def jkpz(message):
    global g_pic_user
    g_pic_user = message.source
    return "请稍候"


client.create_menu({
    "button": [
        {
            "name": "下载中心",
            "sub_button": [
                {
                    "type": "click",
                    "name": "url下载",
                    "key": "url_download"
                },
                {
                    "type": "click",
                    "name": "关键词下载",
                    "key": "key_download"
                }
            ]
        },
        {
            "type": "view",
            "name": "XXXX",
            "url": "http://m.baidu.com/"
        },
    ]})


@robot.subscribe
def new_user(event, session):
    print("openid:%s key:%s ticket:%s" %
          (event.source, event.key, event.ticket))
    users_info = client.get_users_info([event.source, ])
    user = users_info['user_info_list'][0]
    if event.key.startswith('qrscene_'):
        referral = event.key[8:]
    else:
        referral = None
    if session is None or len(session) == 0:
        session['openid'] = event.source
        session['subscribe_key'] = event.key
        session['subscribe_ticket'] = event.ticket
        session['nick_name'] = user['nickname']
        session['referral'] = referral
    return "不做无聊事，何遣有涯生--此为某人自留地"


@robot.key_click("url_download")
def menu_url_download(message, session):
    session["download"] = "url"
    return '请输入下载链接或磁链'


@robot.key_click("key_download")
def menu_key_download(message, session):
    session["download"] = "key"
    return '请输入关键词'


@robot.handler
def autoReply(message, session):
    print(message.source, message.content)
    if session["download"] == "key":
        return key_download(message, session)
    elif session["download"] == "url":
        return url_download(message, session)
    else:
        return("unknown key")


def key_download(message, session):
    return ""


def url_download(message, session):
    return ""


robot.run()
