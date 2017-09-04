import werobot

robot = werobot.WeRoBot(token='Lucy2017')

robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.config["APP_ID"] = "wxba6fbbd0e8bf75bf"
robot.config["APP_SECRET"] = "0f69a6e95110633ad3c49eece688bd1c"
client = robot.client
client.create_menu({
    "button":[
        {
            "name":"个人中心",
            "sub_button":[
				{
					"type":"click",
					"name":"绑定",
					"key":"bind"
				},
                {
                    "type":"click",
                    "name":"我的积分",
                    "key":"score_search"
                },
                {
                    "type":"click",
                    "name":"积分兑换",
                    "key":"redeem"
                },
                {
                    "type":"click",
                    "name":"生成推荐二维码",
                    "key":"gen_qr"
                }
            ]
        },	
		{
			"type":"view",
			"name":"商城",
			"url":"http://m.baidu.com/"
		},
    ]})

@robot.handler
def echo(message):
    return 'Hello World!'

@robot.key_click("bind")
def bind(message):
    return 'you click menu bind.'

@robot.key_click("score_search")
def score_search(message):
    return 'you click menu score_search.'

#robot.run(server='gevent')
robot.run()