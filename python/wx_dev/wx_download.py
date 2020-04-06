##!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import werobot
import threading
import time
import json

g_pic_user = None

robot = werobot.WeRoBot(token='Lucy2017')

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
#测试微信号
robot.config["APP_ID"] = "wx204ef573e97fe056"
robot.config["APP_SECRET"] = "6601eb26017705c8343eeb7a9c5bcaf6"
#robot.config["APP_ID"] = "wxf90ffdab74eb6c6c"
#robot.config["APP_SECRET"] = "83b5fe9743c4e68ee423083d7978ebdf"
#robot.config["ENCODING_AES_KEY"] = "EwECOhBNuQBpllQvCko8KBhge61Mug2ibimC5g5r8dC"
client = robot.client

def catch_send(user_id):
    os.system("raspistill -w 640 -h 360 -o %s.jpg" % user_id)
    with open("%s.jpg"%user_id, "rb") as pic_file:
        ret = client.upload_permanent_media(media_type="image", media_file=pic_file)
        print(type(ret), ret)
        j = eval(str(ret))
    media_id = j['media_id']
    client.send_image_message(user_id=user_id, media_id=media_id)

def thread_wait_send():
    global g_pic_user
    while True:
        if g_pic_user:
            catch_send(user_id = g_pic_user)
            g_pic_user = None
        time.sleep(1)
t=threading.Thread(target=thread_wait_send)
t.start()

@robot.filter('jk')
def jkpz(message):
    global g_pic_user
    g_pic_user = message.source
    return("Please wait a moment.")

@robot.handler
def autoReply(message):
    print(message.source, message.content)
    return("unknown key")

client.create_menu({
    "button":[
        {
            "name":"下载中心",
            "sub_button":[
				{
					"type":"click",
					"name":"url下载",
					"key":"url_download"
				},
                {
                    "type":"click",
                    "name":"关键词下载",
                    "key":"key_download"
                }
            ]
        },	
		{
			"type":"view",
			"name":"XXXX",
			"url":"http://m.baidu.com/"
		},
    ]})

@robot.key_click("url_download")
def url_download(message, session):
    return 'todo'

@robot.key_click("key_download")
def key_download(message):
    return 'todo'

robot.run()
