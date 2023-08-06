import json
from .backends.base import BaseMQHandler


class PrintMQHandler(BaseMQHandler):
    """ 消息打印到控制台
    """
    def handle(self,headers,message):
        print('recive on message.\nheaders:%s\nmessage:%s'%(headers,message))


class JsonMQHandler(BaseMQHandler):
    """ JSON格式消息处理
    """
    def send(self,dest,body, headers=None):
        b=json.dumps(body)
        super().send(dest=dest,body=b,content_type='application/json', headers=headers)
        
    def on_message(self,headers,message):
        content_type = headers.get('content-type',None)
        if content_type and content_type.lower() == 'application/json':
            m = json.loads(message)
        return headers,m
