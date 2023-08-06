# -*- coding:utf-8 -*-
'''
Created on 2021年9月24日

@author: Administrator
'''

import os, sys, logging
from functools import wraps

from tushare.subs.ht_subs.service.covert import datatype_map, convert_ts_model

com_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(com_path)
sys.path.append(f'{com_path}/com')
sys.path.append(f"{com_path}/com/model")
sys.path.append(f"{com_path}/com/interface")
sys.path.append(f"{com_path}/com/libs")

from model import MDPlayback_pb2 as MDPlayback
from model import MDSubscribe_pb2 as MDSubscribe
from interface import mdc_gateway_interface as mdc_gateway_interface
from data_handle import OnRecvMarkertData
from data_handle import get_interface


logger = logging.getLogger(__name__)


class Insight(object):

    def __init__(self, user='', password='', ip='221.131.138.171', port=9362):
        self.user = user
        self.password = password
        self.ip = ip
        self.port = port

        open_trace = False
        open_file_log = False
        open_cout_log = False
        get_interface().init(open_trace, open_file_log, open_cout_log);

        self.login()
        self.start_playback_func = None
        self.start_subscribe_func = None

    def login(self):
        istoken = False
        certfolder = f"{com_path}/com/cert"
        backup_list = mdc_gateway_interface.BackupList()
        get_interface().login(self.ip, self.port, self.user, self.password, istoken, certfolder, backup_list)

    def register_subscribe_func(self, datatypes=[], codes=[]):
        market_data_type_list = []
        for datatype in datatypes:
            datatype = datatype.upper()
            if datatype not in datatype_map:
                raise Exception(f'非法的数据据类型 {datatype}')
            market_data_type_list.append(datatype_map[datatype])
        id_elements = []
        for code in codes:
            id_element = mdc_gateway_interface.SubscribeByIdElement(code, market_data_type_list)
            id_elements.append(id_element)

        def decorator(func):
            # 回调函数
            def on_func(record):
                ts_record, inst_data = convert_ts_model(record)
                func(ts_record, inst_data)
            callback = OnRecvMarkertData()
            callback.OnMarketData = on_func
            get_interface().setCallBack(callback)

            # 订阅接口函数
            def start_func():
                get_interface().subscribeById(MDSubscribe.COVERAGE, id_elements)

                print("input 'stop' to exit >>>")
                line = input()
                if line == 'stop':
                    print("sync: input-->>" + str(line) + ",then exit this sync.")

            self.start_subscribe_func = start_func

            @wraps(func)
            def inner(*args, **kwargs):
                """ should receive a message-value parameter """
                return func(*args, **kwargs)

            return inner
        return decorator

    def register_playback_func(self, datatype='', codes=[], start_time='20191231090000', stop_time='20191231150000'):
        datatype = datatype.upper()
        if datatype.upper() not in datatype_map:
            raise Exception(f'非法的数据据类型 {datatype}')

        def decorator(func):
            # 回调函数
            def on_func(record):
                for inst in record.marketDataStream.marketDataList.marketDatas:
                    ts_record, inst_data = convert_ts_model(inst)
                    func(ts_record, inst_data)
            callback = OnRecvMarkertData()
            callback.OnPlaybackPayload = on_func
            get_interface().setCallBack(callback)

            # 回放接口函数
            def start_func():
                get_interface().playCallback(codes, datatype_map[datatype], MDPlayback.NO_EXRIGHTS, start_time, stop_time)
            self.start_playback_func = start_func

            @wraps(func)
            def inner(*args, **kwargs):
                """ should receive a message-value parameter """
                return func(*args, **kwargs)
            return inner
        return decorator

    def run(self):
        if not self.start_playback_func and not self.start_subscribe_func:
            logger.error('请先配置回调函数')
        if self.start_subscribe_func:
            self.start_subscribe_func()
        if self.start_playback_func:
            self.start_playback_func()


def demo1(username, password):
    app = Insight(user=username, password=password)

    @app.register_subscribe_func(datatypes=['1MIN'], codes=["000001.SH"])
    def print_subscribe_message(ts_record_list=[], ht_record_dict={}, *args, **kwargs):
        """
        订阅数据类型datatypes，并指定codes列表，
            datatype TICK, TRANSACTION, ORDER, 1MIN, 5MIN, 15MIN, 30MIN, 60MIN, 1DAY, 15SECOND
        :param
            ts_record_list:
                数据类型：列表
                字段说明参考 tushare.subs.model.min 和 tushare.subs.model.tick
            ht_record_dict
                数据类型：字典
                字段说明参考华泰的数据格式
        :return:
        """
        print(ts_record_list, ht_record_dict)
        logger.info('用户定义业务代码输出 print_message(%s)' % str(ts_record_list))

    # 程序启动后等待， 输入stop后推出
    app.run()


def demo2(username, password):
    app = Insight(user=username, password=password)

    @app.register_playback_func(datatype='TICK', codes=["000001.SZ"], start_time='2021092413000000', stop_time='20210924150000')
    def print_playback_message(ts_record_list=[], ht_record_dict={}, *args, **kwargs):
        """
        订阅数据类型datatype，并指定codes列表，
            datatype TICK, TRANSACTION, ORDER, 1MIN, 5MIN, 15MIN, 30MIN, 60MIN, 1DAY, 15SECOND
        :param
            ts_record_list:
                数据类型：列表
                字段说明参考 tushare.subs.model.min 和 tushare.subs.model.tick
            ht_record_dict
                数据类型：字典
                字段说明参考华泰的数据格式
        :return:
        """
        print(ts_record_list, ht_record_dict)
        logger.info('用户定义业务代码输出 print_message(%s)' % str(ts_record_list))

    # 数据回访完程序自动结束
    app.run()


if __name__ == '__main__':
    pass

