from djmicroservice.settings import djms_settings
from .client import create_client

#返回一个消息客户端对象
def get_mqclient(subscribes=None,handlercls=None):
    mqsettings = getattr(djms_settings,'MQ',None)
    client = create_client(mqsettings,subscribes,handlercls)
    client.start()
    return client

