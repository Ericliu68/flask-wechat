# -*- coding: utf-8 -*-
import logging

from wxpy.api.chats import Group, Friend, MP


def msg_deal(msg):
    # logging.info(dir(msg))
    if isinstance(msg.chat, Friend):
        logging.info(msg)  # msg.chat.name 打印好友的名字
        # pass

    if isinstance(msg.chat, Group):
        pass
    if isinstance(msg.chat, MP):
        # logging.info(msg)
        # logging.info(msg.type)   msg.articles 文章
        name = (msg.chat.nick_name, msg.chat.name)[msg.chat.nick_name is None]
        logging.info("name::")
        logging.info(name)
        logging.info("articles::")
        logging.info(msg.articles)


def send_msg(data):
    pass
