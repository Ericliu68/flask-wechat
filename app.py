# coding:utf-8


import threading
import time, os
import random
import logging
import json

from flask import Flask, render_template, url_for, request, jsonify

from weixin_status.bot_login import NewBot, check_botname


basepath = os.path.dirname(os.path.realpath(__file__))
bot_list = []  # bot 实例列表

# from flask_apscheduler import APScheduler  # 定时任务模块
# from config import ConfigScheduler  # 导入 定时任务
# 定时任务配置
# app.config.from_object(ConfigScheduler())
# scheduler = APScheduler()
# scheduler.init_app(app)

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)


def json_response(ret, data, msg):
    dict = {"ret": ret}
    if ret > 0:
        dict["object"] = data
    else:
        dict["msg"] = msg
    return jsonify(dict)


def test_msg():
    from weixin_send_msg.send_msg import msg_send

    for bot in bot_list:
        if bot.status == 2:
            bot = bot.bot
            msg_send(bot, None)


@app.route("/weixin/login/<botname>")
def bot_login(botname):
    msg = ""
    qr_base64 = ""
    # 检查是否存在相同名字启动的 bot
    check_num, bot = check_botname(botname, bot_list)
    if check_num == 0:  # 0 新建bot； 1 存在此bot但是没有登录； 2 存在此bot，已经登录
        logging.info("创建新的bot：：{}".format(botname))
        data = NewBot()
        t = threading.Thread(target=data.run, args=())
        t.start()
        data.status = 1
        data.name = botname
        bot_list.append(data)
        while data.qr_base64 == "":
            logging.info("生成二维码中。。。")
            time.sleep(random.random())
        qr_base64 = data.qr_base64

    elif check_num == 1:
        qr_base64 = bot.qr_base64
        logging.info("已经启动，没有登录")

    else:
        msg = "{}::已经在运行".format(botname)
        logging.info("已经登录")

    return render_template("QR.html", name=botname, img=qr_base64, msg=msg)


@app.route("/send_msg", methods=["GET", "POST"])
def send_msg():
    if request.method == "GET":
        try:
            bot = bot_list[0].bot
            my_fr = bot.friends(update=False)  # 只能查出300个好友
            logging.info(my_fr)
        except:
            my_fr = []
        return render_template("sendmsg.html", data=my_fr)
    elif request.method == "POST":

        data = request.form.get("data")
        try:
            data = json.loads(data)
            name = data["username"]
            msg = data["msg"]
            bot = bot_list[0].bot
            my_fr = bot.friends().search(name)[0]
            my_fr.send(msg)
            return json_response(1, None, "success")
        except Exception as e:
            logging.error(e)
            return json_response(1, None, "error")


if __name__ == "__main__":
    # scheduler.start()
    app.run(debug=True)
