# -*- coding: utf-8 -*-


def msg_send(bot, name):
    # pass
    my_friend = bot.friends().search("痕＆殇")[0]
    my_friend.send("Hello, WeChat!")
