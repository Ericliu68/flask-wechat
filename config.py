# -*- coding: utf-8 -*-


class ConfigScheduler(object):
    JOBS = [
        {
            "id": "send_msg",
            "func": "__main__:test_msg",
            "args": None,
            "trigger": "interval",
            "seconds": 60,
        }
    ]
