from abc import ABCMeta,abstractmethod,abstractproperty


class BaseDiscover:
    ''' 服务发现者抽象类
    '''
    __metaclass__ = ABCMeta

    def __init__(self,*args,**kwargs):
        pass 

    @abstractmethod
    def register(self,service,url):
        ''' 微服务注册
        @service 服务名
        @url 服务url;如果@resource不是None,是资源url 
        @resource 资源名
        '''
        pass

    @abstractmethod
    def get(self,service):
        ''' 获取服务/资源url
        @service 服务名
        @resource 资源名
        '''
        pass



class StaticDiscover(BaseDiscover):
    ''' 静态服务发现
    '''
    def __init__(self,options):
        self._services = options.get('SERVICES',None)

    def register(self,service,url):
        return True

    def get(self,service):
        if not isinstance(service,str) or self._services is None:
            return None
        url = None
        for item in self._services:
            if item[0] == service:
                url = item[1]
                break
        return url        

