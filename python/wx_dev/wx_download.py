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
robot.config["APP_ID"] = "wxf90ffdab74eb6c6c"
robot.config["APP_SECRET"] = "83b5fe9743c4e68ee423083d7978ebdf"
robot.config["ENCODING_AES_KEY"] = "EwECOhBNuQBpllQvCko8KBhge61Mug2ibimC5g5r8dC"
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

@robot.handler
def autoReply(message):
    print(message.source, message.content)
    if message.content == 'jkpz':
        global g_pic_user
        g_pic_user = message.source
        # catch_send(message.source)
    return "hello"

# client.create_menu({
#     "button":[
#         {
#             "name":u"个人中心",
#             "sub_button":[
# 				{
# 					"type":"click",
# 					"name":u"绑定",
# 					"key":"bind"
# 				},
#                 {
#                     "type":"click",
#                     "name":u"我的积分",
#                     "key":"score_search"
#                 },
#                 {
#                     "type":"click",
#                     "name":u"积分兑换",
#                     "key":"redeem"
#                 },
#                 {
#                     "type":"click",
#                     "name":u"生成推荐二维码",
#                     "key":"gen_qr"
#                 }
#             ]
#         },	
# 		{
# 			"type":"view",
# 			"name":u"商城",
# 			"url":"http://m.baidu.com/"
# 		},
#     ]})
# @robot.handler
# def echo(message):
#     print(message)
#     return 'Something is wrong'

# @robot.key_click("bind")
# def bind(message, session):
#     return 'you aleady bind. your ticket is %s' % session['subscribe_ticket']

# @robot.key_click("score_search")
# def score_search(message):
#     return 'you click menu score_search.'

# @robot.key_click("redeem")
# def redeem(message):
#     return 'you click menu redeem.'

# @robot.key_click("gen_qr")
# def gen_qr(message, session):
#     data = '{"expire_seconds": 604800, "action_name": "QR_STR_SCENE", "action_info": {"scene": {"scene_str": "%s"}}}' % session['openid']
#     js = client.create_qrcode(data)
#     ticket = js['ticket']
#     #client.show_qrcode(ticket)
#     os.system("wget https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s -O tmp.jpg" % ticket)
#     #return "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" % ticket

#     print(client.token)
#     with open('tmp.jpg') as f:
#         js = client.upload_media(media_type='image', media_file=f)
#     media_id = js['media_id']
#     return werobot.replies.ImageReply(message=message, media_id = media_id)

# @robot.subscribe
# def new_user(event, session):
#     print("openid:%s key:%s ticket:%s" %(event.source, event.key, event.ticket))
#     users_info = client.get_users_info([event.source,])
#     user = users_info['user_info_list'][0]
#     if event.key.startswith('qrscene_'):
#         referral = event.key[8:]
#     else:
#         referral = None
#     if session is None or len(session) == 0:
#         session['openid'] = event.source
#         session['subscribe_key'] = event.key
#         session['subscribe_ticket'] = event.ticket
#         session['nick_name'] = user['nickname']
#         session['referral'] = referral
#     return 'Welcome to this site.\n' + \
#            'Your Referrals is %s.\n' % referral + \
#            'bala, bala...'

robot.run()
