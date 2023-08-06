import stomp
from djmicroservice.utils import create_objectid
from .base import BaseMQ,logger

class MQListener(stomp.ConnectionListener):
    """ ActiveMQ listener
    """

    def __init__(self,engine):
        self._engine = engine

    def on_connecting(self, host_and_port):
        super().on_connecting(host_and_port)
        logger.info('ActiveMQ connecting.')

    def on_connected(self, headers, body):
        super().on_connected(headers,body)
        logger.info('ActiveMQ connected.')

    def on_disconnected(self):
        super().on_disconnected()
        logger.info('ActiveMQ disconnected.')

    def on_heartbeat_timeout(self):
        super().on_heartbeat_timeout()
        logger.info('ActiveMQ heartbeat timeout.')

    def on_error(self, headers, message):
        super().on_error(headers,message)
        logger.warn('received an error.\nheaders:%s\nmessage:%s' %(headers, message))

    def on_message(self, headers, message):
        logger.debug('received an message.\nheaders:%s\nmessage:%s' %(headers, message))
        self._engine.distribute(headers,message)


class ActiveMQ(BaseMQ):
    """ ActiveMQ 引擎 
    """
    def __init__(self,options):
        super().__init__(options=options)
        params ={
            'host_and_ports':options.get('SERVERS'),
            'prefer_localhost':options.get('PREFER_LOCALHOST',True),
            'try_loopback_connect':options.get('TRY_LOOPBACK_CONNECT',True),
            'reconnect_sleep_initial':options.get('RECONNECT_SLEEP_INITIAL',0.1),
            'reconnect_sleep_increase':options.get('RECONNECT_SLEEP_INCREASE',0.5),
            'reconnect_sleep_jitter':options.get('RECONNECT_SLEEP_JITTER',0.1),
            'reconnect_sleep_max':options.get('RECONNECT_SLEEP_MAX',60.0),
            'reconnect_attempts_max':options.get('RECONNECT_ATTEMPTS_MAX',3),
            'use_ssl':options.get('USE_SSL',False),
            'ssl_key_file':options.get('SSL_KEY_FILE',None),
            'ssl_cert_file':options.get('SSL_CERT_FILE',None),
            'ssl_ca_certs':options.get('SSL_CA_CERTS',None),
            'ssl_cert_validator':options.get('SSL_CERT_VALIDATOR',None),
            'wait_on_receipt':options.get('WAIT_ON_RECEIPT',False),
            'ssl_version':options.get('SSL_VERSION',stomp.connect.DEFAULT_SSL_VERSION),
            'timeout':options.get('TIMEOUT',None),
            'keepalive':options.get('KEEPALIVE',None),
            'auto_decode':options.get('AUTO_DECODE',True),
            #'encoding':options.get('ENCODING','UTF-8'),
            'auto_content_length':options.get('AUTO_CONTENT_LENGTH',True),
            #'recv_bytes':options.get('RECV_BYTES',1024)
        }
        self._conn = stomp.Connection(**params)
        self._conn.set_listener('', MQListener(self))        

    def start(self):
        super().start()
        user = self._options.get('USER')
        passwd = self._options.get('PASSWORD')
        if not self._conn.is_connected():
            self._conn.start()
            self._conn.connect(user,passwd,wait=True)
        
    def stop(self):
        super().stop()
        self._conn.disconnect()
        self._conn.stop()

    def add_handler(self,dest,handler):
        super().add_handler(dest,handler)
        self._conn.subscribe(dest,id=create_objectid())

    def send(self,dest,body,content_type=None, headers=None):
        self._conn.send(dest,body,content_type, headers)
        

    def get_dest(self,headers,message):
        dest = headers.get('destination',None)    
        return dest

    def is_connected(self):
        return self._conn.is_connected()
