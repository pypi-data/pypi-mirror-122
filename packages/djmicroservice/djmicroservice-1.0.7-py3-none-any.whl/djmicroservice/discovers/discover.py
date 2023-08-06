from djmicroservice.settings import djms_settings
from djmicroservice.utils import import_object

class Discover():
    """ 服务发现
    """
    def __init__(self,setting):
        self._setting = setting
        backend = import_object(self._setting.DISCOVER.get('ENGINE'))
        options = self._setting.DISCOVER.get('OPTIONS')
        self._engine = backend(options)

    def register(self,service=None,url=None):
        """ 注册服务
        """
        if service is None or url is None:
            service = self._setting.NAME
            url = self._setting.URL
        return self._engine.register(service,url)

    def get_url(self,service):
        """ 获取服务的根URL
        """    
        return self._engine.get(service)


default_discover = Discover(djms_settings)