from djmicroservice.utils import import_object
from .backends import BaseMQ,BaseMQHandler
from .handlers import PrintMQHandler


class MQClient():
    """ 消息队列客户端
    """
    def __init__(self,options,backendcls,handlercls,subscribes=None):
        self._options = options
        if not issubclass(backendcls,BaseMQ):
            raise ValueError("'backendcls' must subclass of 'BaseMQ'.")
        self._backend = backendcls(options) 
        self._handlercls = handlercls
        if isinstance(subscribes,str):
            subscribes = [subscribes]     
        self._subscribes = subscribes or []

    def subscribe(self,dest):
        """ 订阅消息
        """
        if not self._backend.is_connected():
            return False
        self._backend.add_handler(dest,self._handlercls)    
        return True


    def start(self):
        """ 启动客户端
        """
        if not self._backend.is_connected():
            self._backend.start()
            for dest in self._subscribes:
                self.subscribe(dest)

    def close(self):
        """ 关闭客户端
        """
        if self._backend.is_connected():
            self._backend.stop()

    def send(self,dest,body,content_type=None, headers=None):
        self._backend.send(dest,body,content_type, headers)



def create_client(settings,subscribes=None,handlercls=None):
    enginename = settings.get('ENGINE',None)
    if enginename is None:
        return None
    backendcls = import_object(enginename)
    if backendcls is None:
        return None
    options = settings.get('OPTIONS',{})
    handlercls = handlercls or PrintMQHandler
    return MQClient(options,backendcls,handlercls,subscribes)


