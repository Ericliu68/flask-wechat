# -*- coding: utf-8 -*-


class Config_Scheduler(object):
    JOBS = [
        {
            'id': 'send_msg',
            'func': '__main__:test_msg',
            'args': None,
            'trigger': 'interval',
            'seconds': 60
        }
    ]
