# -*- coding: utf-8 -*-

import os
import datetime
import socket
import json
import ctypes

try:
    from urllib.parse import (quote,
                              unquote)
except ImportError:
    from urllib import (quote,
                        unquote)


def server_setup(user_ip, user_port):
    # 隐藏窗口
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)

    server_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_.bind((user_ip, user_port))
    server_.listen(5)
    return server_


def server_watch(server, logger, **kwargs):
    valid_ip = kwargs.get('valid_ip', None)
    remote_launcher = kwargs.get('remote_launcher', None)

    while True:
        conn, addr = server.accept()
        msg = unquote(conn.recv(1024).decode('utf-8'))  # json格式的str
        peer_name = conn.getpeername()  # peer_name是个tuple，peer_name[0]是ip，peer_name[1]是端口号
        now_dt = str(datetime.datetime.now())

        logger.info('{0}, visitor: {1}:{2}'.format(now_dt, peer_name[0], peer_name[1]))  # sock_name

        params = json.loads(msg)
        msg_type = params['msg_type']

        if valid_ip is not None and peer_name[0] in valid_ip:
            logger.info(params)

            # 1. 运行普通py脚本的msg
            if 'run_py' == msg_type:
                logger.info('执行py文件')
                # remote_py_file_path = '..//workstation//start_programs.py'
                remote_file = remote_launcher

                command = '''start cmd /k " python {remote_py_file_path} "{extra_param}" && exit"'''
                param_json_str = json.dumps(params)
                param_json_str = param_json_str.replace('"', '$')
                command = command.format(**{'remote_py_file_path': remote_file,
                                            'extra_param': param_json_str})

                logger.info(command)
                os.system(command)
