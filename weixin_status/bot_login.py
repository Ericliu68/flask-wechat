# coding:utf-8

import base64

from wxpy import *

from msg_deal import msg_deal


# 检查bot 状态
def check_botname(botname, bot_list):
    for bot in bot_list:
        if bot.name == botname:
            if bot.status == 1:
                return 1, bot
            elif bot.status == 3:
                bot_list.remove(bot)
                return 0, ""
            return 2, bot

    return 0, ""


# 启动bot实例，生成二维码
class NewBot(object):
    qr_base64 = ""
    name = ""
    status = 0  # 0不存在此bot； 1 存在此bot但是没有登录； 2 存在此bot，已经登录； 3 退出
    bot = None
    friends_list = []
    groups_list = []
    mps = []

    def run(self):
        # self.status = 1
        self.bot = Bot(logout_callback=self.logout_call_back, qr_callback=self.qr_call_back)
        self.status = 2
        # self.bot = bot
        bot = self.bot
        logging.info("登陆成功")
        self.friends_list = bot.friends()  # 最大获取300个好友
        self.groups_list = bot.groups()
        self.mps = bot.mps()

        @bot.register()
        def message_handle(msg):
            msg_deal.msg_deal(msg)
            # logging.info(msg.type)   # msg.type 区分聊天的类型，是文本还是图片

        bot.join()
        # embed()

    def logout_call_back(self):
        self.status = 3
        logging.info("退出了")

    def qr_call_back(self, uuid, status, qrcode):
        self.qr_base64 = str(base64.b64encode(qrcode))[2:-1]
