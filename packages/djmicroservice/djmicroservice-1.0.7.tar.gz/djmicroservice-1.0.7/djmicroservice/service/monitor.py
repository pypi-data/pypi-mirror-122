from multiprocessing.managers import BaseManager


#默认服务管理进程通信地址
DEFAULT_SERVICE_MONITOR_ADDR = ('127.0.0.1',56560)
#默认通信密钥
DEFAULT_SERVICE_MONITOR_AUTHKEY = b'0\xca\xc4/q{\xa3Q\x8b\xf9\x93\xba\x14\x01on+(C2)\xe1iB\xba\x1f\xa5\xb6}\xf1\xedH'


class ServiceMonitor():
    '''后台服务监控
    '''
    def __init__(self,address=None, authkey=None,services=None):
        pass