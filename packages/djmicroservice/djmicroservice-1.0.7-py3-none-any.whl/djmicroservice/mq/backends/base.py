import logging
from abc import ABCMeta,abstractmethod,abstractproperty
from django.utils.datastructures import ImmutableList, MultiValueDict

logger = logging.getLogger('djmicroservice.mq.backends')

class BaseMQHandler():
    """ 消息处理器基类
    """
    def __init__(self,mq):
        if not isinstance(mq,BaseMQ):
            raise ValueError("mq must is 'BaseMQ' type.")
        self._mq = mq     

    def send(self,dest,body,content_type=None, headers=None):
        """ 发送消息
        """
        self._mq.send(dest,body,content_type, headers) 

    def on_message(self,headers, body):
        """ 收到消息时被调，返回(headers,body)
        """    
        return headers,body

    def handle(self, headers, body):
        pass       

class BaseMQ():
    """ 消息队列引擎基类
    """
    __metaclass__ = ABCMeta

    def __init__(self,options):
        self._options = options
        self._handlers = MultiValueDict()

    def start(self):
        """ 启动引擎，系统开始时被调用
        """
        logger.info('MQ engine start.')
        return True

    def stop(self):
        """ 停止引擎，系统停止时被调用
        """
        logger.info('MQ engine stop.')
        return True

    def add_handler(self,dest,handler):
        """ 添加消息处理类
        """
        if not isinstance(dest,str):
            raise ValueError("'dest' must is 'str' type.")
        if not issubclass(handler,BaseMQHandler):
            raise ValueError("'handler' must is 'BaseMQHandler' type.")   
        logger.info('Add message handler:(%s=>%s)'%(dest,type(handler)))     
        self._handlers.appendlist(dest,handler)


    @abstractmethod
    def send(self,dest,body,content_type=None, headers=None):
        """ 抽象方法，发送消息
        """
        pass  

    def distribute(self,headers,message):
        """ 分发消息到消息处理器
        """
        dest = self.get_dest(headers,message)
        handlers = self._handlers.getlist(dest)         
        if not handlers:
            logger.warn('Not found message handler .\ndest:%s\nheaders:%s\nmessage:%s'%(dest,headers,message))
            return 

        for handlercls in handlers:
            handler = handlercls(self)
            logger.debug("Distribute message to handler. \ndest:%s\nheaders:%s\nmessage:%s"%(dest,headers,message))            
            (h,m) = handler.on_message(headers,message)
            handler.handle(h,m)


    @abstractmethod
    def get_dest(self,headers,message):
        """ 抽象方法，返回一个字符串，以确定消息的处理器，对应配置MQ.HANDLERS的KEY.
        """
        pass  

    @abstractmethod
    def is_connected(self):
        """ 抽象方法，返回引擎到消息服务器的连接是否在线。
        """
        return False