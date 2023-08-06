#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from happy_python.happy_config import HappyConfigBase
from happy_python.happy_exception import HappyPyException


def param_check(zy_config_value, zy_config_key):
    if zy_config_value == '':
        raise HappyPyException("配置文件中 " + zy_config_key + " 字段为空")


class LoadCustomizeZymodConfigParser(HappyConfigBase):
    pass


class LoadPublicZymodConfigParser(HappyConfigBase):
    def __init__(self):
        super().__init__()

        self.section = 'zymod'
        self.mod_name = ''
        self.active = ''
        self.agent_host = ''
        self.agent_port = ''
        self.debug = ''
        self.dry_run = ''
        self.interval = ''
        self.token = ''
        self.host = ''
        self.headers = ''
        # self.unit = ''
        self.chinese_name = ''
        self.mod_type = ''
        self.event_report = ''
        self.notice_report = ''
        self.alert_threshold = ''
        self.warning_threshold = ''
