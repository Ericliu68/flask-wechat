# coding:utf-8


import threading
import time, os
import random
import logging


basepath = os.path.dirname(os.path.realpath(__file__))


# import sys
# sys.path.append('{}{}msg_deal'.format(basepath,os.sep))
# sys.path.append('{}{}weixin_status'.format(basepath,os.sep))


from flask_apscheduler import APScheduler   # 定时任务模块
from flask import Flask, render_template, url_for, request, jsonify


# 导入创建bot示例的类
from weixin_status.bot_login import New_Bot, check_botname


# from config import Config_Scheduler  # 导入 定时任务

logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)


def jsonResponse(ret, data, msg):

    dict = {'ret': ret}
    if ret > 0:
        dict['object'] = data
    else:
        dict['msg'] = msg
    return jsonify(dict)


def test_msg():
    from weixin_send_msg.send_msg import msg_send
    for bot in bot_list:
        if bot.status == 2:
            bot = bot.bot
            msg_send(bot, None)

# 定时任务配置
# app.config.from_object(Config_Scheduler())
# scheduler = APScheduler()
# scheduler.init_app(app)

bot_list = []   # bot 实例列表


@app.route('/weixin/login/<botname>')
def bot_login(botname):
    # pass
    # logging.info('开始')
    msg = ''
    qr_base64 = ''
    # 检查是否存在相同名字启动的 bot
    check_num, bot = check_botname(botname, bot_list)
    if check_num == 0:   # 0 新建bot； 1 存在此bot但是没有登录； 2 存在此bot，已经登录
        logging.info('创建新的bot：：{}'.format(botname))
        data = New_Bot()
        t = threading.Thread(target=data.run, args=())
        t.start()
        data.status = 1
        data.name = botname
        bot_list.append(data)
        while data.qr_base64 == '':
            logging.info('生成二维码中。。。')
            time.sleep(random.random())
        qr_base64 = data.qr_base64

    elif check_num == 1:
        qr_base64 = bot.qr_base64
        logging.info('已经启动，没有登录')

    else:
        msg = '{}::已经在运行'.format(botname)
        logging.info('已经登录')

    return render_template('QR.html', name=botname, img=qr_base64, msg=msg)


@app.route('/sendmsg', methods=['GET', 'POST'])
def sendmsg():
    if request.method == 'GET':
        try:
            bot = bot_list[0].bot
            my_fr = bot.friends(update=False)  # 只能查出300个好友
            logging.info(my_fr)
        except:
            my_fr = []
        return render_template('sendmsg.html', data=my_fr)
    elif request.method == 'POST':

        data = request.form.get('data')
        try:
            import json
            data = json.loads(data)
            name = data['username']
            msg = data['msg']
            bot = bot_list[0].bot
            my_fr = bot.friends().search(name)[0]
            my_fr.send(msg)
            return jsonResponse(1, None, 'success')
        except:
            return jsonResponse(1, None, 'error')

# @app.route('/img')
# def Sendimg():
#     return render_template('img.html')


if __name__ == '__main__':
    # scheduler.start()
    app.run(debug=False)
