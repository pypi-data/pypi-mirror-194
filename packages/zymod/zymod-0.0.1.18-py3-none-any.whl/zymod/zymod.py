#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import json
import signal
import time
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

from happy_python import dict_to_pretty_json

import grpc
from happy_python import HappyLog, HappyConfigParser

from proto import zhiyan_rpc_pb2
from proto import zhiyan_rpc_pb2_grpc
from zymod.zymod_config import LoadPublicZymodConfigParser, param_check


# noinspection PyUnusedLocal
def interrupt_from_keyboard_handler(signum, frame):
    print('\n检测到用户发送终止信号，退出程序中......')
    exit(1)


def get_linux_kernel_version():
    f = open("/proc/version", encoding="utf-8")
    version = f.read().split(" ")[2]
    f.close()
    split_version = version.split(".")
    return split_version[0] + "." + split_version[1]


def status_translate(event_status):
    status_int = "关闭" if event_status == 0 else "开启"
    return status_int


def build_threshold(mut_list: list, reg, split_value: str):
    split_value = split_value.split(reg)
    for i in split_value:
        mut_list.append(i)


def event_threshold_analysis(value: str, value_type: str):
    mut_list = []
    split_value = ":" if value_type == "rows" else ","
    split_vec = value.split(split_value)

    for i in split_vec:
        if i.__contains__("},"):
            build_threshold(mut_list, '},', i)
        elif i.__contains__(",") and not i.__contains__("{") and not i.__contains__("}"):
            build_threshold(mut_list, ',', i)
        else:
            mut_list.append(i.replace('{', '').replace('}', ''))

    if value_type == "rows":
        rows_list = []
        for w in range(int(len(mut_list) / 2)):
            s = ""
            s += str(mut_list[2 * w])
            s += str(':')
            s += str(mut_list[(2 * w) + 1])
            rows_list.append(s)
        return rows_list
    else:
        return mut_list


def build_event(event_level, module_name: str, filed_name, filed_value, threshold_value, summary: str,
                description: str):
    describe_replace = description.replace("column", filed_name)
    summary_replace = summary.replace("column", filed_name)

    describe_format = '%s模块%s' % (module_name, describe_replace)
    summary_format = '%s模块%s' % (module_name, summary_replace)

    return {"level": event_level, "summary": summary_format, "description": describe_format,
            "metric": {"name": filed_name, "value": filed_value, "threshold_value": threshold_value}}


def upload_letsencrypt_event(content: dict, agent_host: str, agent_port: str, mod_name: str, host: str):
    fn_name = 'upload_letsencrypt_event'

    hlog = HappyLog.get_instance()
    hlog.enter_func(fn_name)

    json_str_content = dict_to_pretty_json(content)

    hlog.debug('zymod：正在上传到agent.....')
    channel = grpc.insecure_channel(
        agent_host + ':' + agent_port)

    try:
        client = zhiyan_rpc_pb2_grpc.ZhiYanServiceStub(channel)
        response = client.zyevent(zhiyan_rpc_pb2.ZhiYanEventRequest(
            mod_name=mod_name,
            time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
            host=host,
            event=json_str_content
        ))

        hlog.info('code:' + response.code + '\tmessage:' + response.message)
    except Exception as ex:
        hlog.error('code:' + "1" + '\tmessage:' + 'Agent连接失败,十秒后进行下一次尝试\tErrorMessage:' + str(ex))

    hlog.exit_func(fn_name)


class Zymod:
    hlog = HappyLog.get_instance()
    mod_conf: dict[Any, Any]
    parser: ArgumentParser

    def __init__(self, mod_config: Path, is_dry_run_from_cmd_args, is_verbose_from_cmd_args):
        signal.signal(signal.SIGINT, interrupt_from_keyboard_handler)

        self.hlog = HappyLog.get_instance(str(mod_config))

        self.is_dry_run = True if is_dry_run_from_cmd_args else None
        self.is_verbose = True if is_verbose_from_cmd_args else None

        self.public_zymod_config = LoadPublicZymodConfigParser()
        HappyConfigParser.load(str(mod_config), self.public_zymod_config)
        self.mod_config_path = str(mod_config)

    @staticmethod
    def event_level_transformation(event_level: str):
        if event_level == "通知":
            return 0
        elif event_level == "警告":
            return 1
        elif event_level == "警报":
            return 2

    def event_status(self):
        hlog = HappyLog.get_instance()
        hlog.enter_func("event_status")

        notice_status = 1 if self.public_zymod_config.notice_report == "true" else 0
        event_status = 1 if self.public_zymod_config.event_report == "true" else 0
        alert_status = 1 if len(self.public_zymod_config.alert_threshold) != 0 else 0
        warning_status = 1 if len(self.public_zymod_config.warning_threshold) != 0 else 0

        hlog.info("事件上传%s（通知：%s、警报：%s、警告：%s）" % (
            status_translate(event_status), status_translate(notice_status), status_translate(alert_status),
            status_translate(warning_status)))

        event_status = [event_status, notice_status, alert_status, warning_status]

        return event_status

    def event_judge(self, json_value, threshold_value_format, event_level, threshold_key, threshold_value, summary,
                    description, event_type):
        hlog = HappyLog.get_instance()
        hlog.enter_func("event_judge")
        if json_value >= threshold_value_format:
            if event_type == "report":
                self.upload_event(build_event(
                    event_level=self.event_level_transformation(event_level),
                    module_name=self.public_zymod_config.mod_name,
                    filed_name=threshold_key,
                    filed_value=format(float(json_value), '.2f'),
                    threshold_value=format(threshold_value),
                    summary=summary,
                    description=description
                ))
            elif event_type == "log":
                hlog.info("事件等级：%s，事件标题：%s，事件内容：%s，触发字段：%s,触发值：%s,字段阈值：%s" % (
                    event_level, summary, description, threshold_key, json_value, threshold_value))
            return 1
        else:
            return 0

    def event_trigger(self, value: str, json_object, event_level: str, summary: str, event_type):
        event_status = 0
        value_type = "rows" if value.__contains__('=') else "single"
        split_content = event_threshold_analysis(value=value, value_type=value_type)
        if value_type == "single":
            for i in split_content:
                split = i.split(":")
                threshold_key = split[0]
                threshold_value = float(split[1])
                json_value = float(json_object[threshold_key])
                threshold_value_format = threshold_value * 100.00 if str(threshold_value).startswith(
                    "0.") else threshold_value

                event_status = self.event_judge(json_value, threshold_value_format, event_level, threshold_key,
                                                threshold_value, summary, str(json_object).replace("'", "\""),
                                                event_type)
        elif value_type == "rows":
            for i in split_content:
                split = i.split(":")
                threshold_key = split[0]
                threshold_value = split[1]
                split_threshold_value = threshold_value.split(",")

                if threshold_value.__contains__("="):
                    for s in split_threshold_value:
                        split = s.split("=")
                        single_threshold_key = split[0]
                        single_threshold_value = float(split[1])
                        json_value = float(json_object[threshold_key])
                        threshold_value_format = single_threshold_value * 100.00 if str(
                            single_threshold_value).startswith("0.") else single_threshold_value
                        filed = "'%s'" % single_threshold_key

                        if str(json_object).__contains__(filed):
                            event_status = self.event_judge(json_value, threshold_value_format, event_level,
                                                            threshold_key,
                                                            single_threshold_value, summary,
                                                            str(json_object).replace("'", "\""), event_type)
                else:
                    json_value = float(json_object[threshold_key])
                    threshold_value_format = float(threshold_value) * 100.00 if str(
                        threshold_value).startswith("0.") else float(threshold_value)
                    event_status = self.event_judge(json_value, threshold_value_format, event_level, threshold_key,
                                                    threshold_value, summary, str(json_object).replace("'", "\""),
                                                    event_type)
        return event_status

    def event(self, status_list: dict, json_object, summary: str):
        global thresholds
        global level
        status = 0
        event_type = "report" if status_list[0] == 1 else "log"

        for i in range(1, 4):
            if i == 1 and status_list[1] == 1:
                self.event_trigger(self.public_zymod_config.alert_threshold, json_object, '通知', summary, event_type)
            if i == 2 and status_list[2] == 1:
                status = self.event_trigger(self.public_zymod_config.alert_threshold, json_object, '警报', summary,
                                            event_type)
            elif i == 3 and status == 0 and status_list[3] == 1:
                self.event_trigger(self.public_zymod_config.warning_threshold, json_object, '警告', summary, event_type)

    def register(self, content: dict):
        while True:
            # 第一次注册
            register_code = self.register_module(content=content)
            if not register_code:
                # 不成功则每隔10秒进行一次注册
                while True:
                    time.sleep(10)
                    upload_code = self.upload_data(content=content)
                    # 注册成功取消循环
                    if upload_code:
                        break
            else:
                break

    def register_module(self, content: dict) -> bool:
        register = True

        fn_name = 'mod_send_request_grpc'

        hlog = HappyLog.get_instance()
        hlog.enter_func(fn_name)

        hlog.var('name', self.public_zymod_config.mod_name)
        param_check(self.public_zymod_config.mod_name, 'mod_name')
        hlog.var('datetime', int(time.time()))

        json_str_content = dict_to_pretty_json(content)

        hlog.debug('content=\n%s' % json_str_content)

        if bool(self.is_dry_run):
            hlog.debug('zymod：试运行中，不进行注册.....')
        else:
            hlog.debug('zymod：正在上传到agent.....')
            channel = grpc.insecure_channel(
                self.public_zymod_config.agent_host + ':' + str(self.public_zymod_config.agent_port))

            param_check(self.public_zymod_config.agent_host, 'agent_host')
            param_check(self.public_zymod_config.agent_port, 'agent_port')

            try:
                client = zhiyan_rpc_pb2_grpc.ZhiYanServiceStub(channel)

                response = client.zyregistermod(zhiyan_rpc_pb2.ZhiYanRegisterModuleRequest(
                    name=str(self.public_zymod_config.mod_name),
                    content=str(json_str_content),
                    token=str(self.public_zymod_config.token),
                    host=str(self.public_zymod_config.host),
                    config=str({
                        "host": self.public_zymod_config.host,
                        "active": self.public_zymod_config.active,
                        "debug": self.public_zymod_config.debug,
                        "dry_run": self.public_zymod_config.dry_run,
                        "interval": self.public_zymod_config.interval,
                        "mod_name": self.public_zymod_config.mod_name,
                        "headers": self.public_zymod_config.headers,
                        # "unit": self.public_zymod_config.unit,
                        "chinese_name": self.public_zymod_config.chinese_name,
                        "mod_type": self.public_zymod_config.mod_type,
                    }),
                ))
                hlog.info('code:' + response.code + '\tmessage:' + response.message)

                if response.code != '1':
                    register = True
                else:
                    register = False
            except Exception:
                hlog.error('code:' + "1" + '\tmessage:' + 'Agent连接失败,十秒后进行下一次注册')
                register = False

        hlog.exit_func(fn_name)

        return register

    def upload_event(self, content: dict):
        global fn
        fn_name = 'upload_event'

        hlog = HappyLog.get_instance()
        hlog.enter_func(fn_name)

        json_str_content = dict_to_pretty_json(content)

        if bool(self.is_dry_run):
            hlog.debug('zymod：在不做任何更改的情况下试运行.....')
        else:
            hlog.debug('zymod：正在上传到agent.....')
            channel = grpc.insecure_channel(
                self.public_zymod_config.agent_host + ':' + str(self.public_zymod_config.agent_port))

            try:
                client = zhiyan_rpc_pb2_grpc.ZhiYanServiceStub(channel)
                response = client.zyevent(zhiyan_rpc_pb2.ZhiYanEventRequest(
                    mod_name=str(self.public_zymod_config.mod_name),
                    time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                    host=str(self.public_zymod_config.host),
                    event=str(json_str_content)
                ))

                hlog.info('code:' + response.code + '\tmessage:' + response.message)
            except Exception as ex:
                hlog.error('code:' + "1" + '\tmessage:' + 'Agent连接失败,十秒后进行下一次尝试\tErrorMessage:' + str(ex))

        hlog.exit_func(fn_name)

    def upload_data(self, content: dict) -> bool:
        global fn
        register = True

        fn_name = 'mod_send_request_grpc'

        hlog = HappyLog.get_instance()
        hlog.enter_func(fn_name)

        hlog.var('name', self.public_zymod_config.mod_name)
        param_check(self.public_zymod_config.mod_name, 'mod_name')
        hlog.var('datetime', int(time.time()))

        json_str_content = dict_to_pretty_json(content)

        hlog.debug('content=\n%s' % json_str_content)

        if bool(self.is_dry_run):
            hlog.debug('zymod：在不做任何更改的情况下试运行.....')
        else:
            hlog.debug('zymod：正在上传到agent.....')
            channel = grpc.insecure_channel(
                self.public_zymod_config.agent_host + ':' + str(self.public_zymod_config.agent_port))

            param_check(self.public_zymod_config.agent_host, 'agent_host')
            param_check(self.public_zymod_config.agent_port, 'agent_port')

            try:
                client = zhiyan_rpc_pb2_grpc.ZhiYanServiceStub(channel)
                response = client.zymod(zhiyan_rpc_pb2.ZhiYanRequest(
                    mod_name=str(self.public_zymod_config.mod_name),
                    time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                    host=str(self.public_zymod_config.host),
                    metrices=str(json_str_content),
                ))

                time.sleep(float(self.public_zymod_config.interval))

                hlog.info('code:' + response.code + '\tmessage:' + response.message)

                if response.code == '1':
                    register = False
                elif response.code == '10':
                    replace_json = response.message.replace('\\', '').replace('"{', '{').replace('}"', '}')
                    format_json = json.loads(replace_json)

                    items = format_json['Config'].items()

                    conf = configparser.ConfigParser()
                    conf.read(self.mod_config_path)
                    for key, value in items:
                        conf.set("zymod", str(key), str(value).replace('\'', '"').replace('%', '%%'))
                        fn = open(self.mod_config_path, 'w')
                        conf.write(fn)

                    fn.close()

                    register = False
                else:
                    register = True
            except Exception as ex:
                hlog.error('code:' + "1" + '\tmessage:' + 'Agent连接失败,十秒后进行下一次尝试\tErrorMessage:' + str(ex))
                register = False

        hlog.exit_func(fn_name)

        return register

    @staticmethod
    def build_help_parser(prog: str, description: str, version: str, mod_config_file_path: str) -> ArgumentParser:
        parser = ArgumentParser(prog=prog + ' ' + version, description=description)
        parser.add_argument('-c',
                            '--conf',
                            help='指定智眼模块配置文件',
                            dest='mod_conf',
                            type=str,
                            default=mod_config_file_path)
        parser.add_argument('-n',
                            '--dry-run',
                            help='在不做任何更改的情况下试运行，通常和"-v"参数一起使用',
                            dest='dry_run',
                            action='store_true')
        parser.add_argument('-v',
                            '--verbose',
                            help='显示详细信息',
                            dest='verbose',
                            action='store_true')
        parser.add_argument('-V',
                            '--version',
                            help='显示版本信息',
                            action='version',
                            version='zymod version: %(prog)s/v' + version)

        return parser

    @staticmethod
    def build_help(prog: str, description: str, version: str, mod_config_file_path: str):
        parser = Zymod.build_help_parser(prog=prog,
                                         description=description,
                                         version=version,
                                         mod_config_file_path=mod_config_file_path,
                                         )
        return parser.parse_args()

    @staticmethod
    def build_help_with_parser(parser: ArgumentParser):
        return parser.parse_args()
