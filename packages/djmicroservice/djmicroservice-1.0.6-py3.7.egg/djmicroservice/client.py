from django.utils.translation import ugettext as _
from simple_rest_client import exceptions
from simple_rest_client.api import API
from simple_rest_client.models import Response
from djmicroservice.settings import djms_settings
from djmicroservice.discovers import default_discover


class AuthJwt():
    """ jwt认证
    """
    def __init__(self,root_url,obtain=None,refresh=None,verify=None,timeout=2):
        self._api= API(api_root_url=root_url,
                       json_encode_body=True,
                       headers={'Content-Type': 'application/json'},
                       append_slash=True,
                       timeout=timeout)
        self._obtain = obtain or 'auth_jwt'
        self._refresh = refresh or 'auth_jwt_refresh'
        self._verify = verify or 'auth_jwt_verify'        
        self._api.add_resource(resource_name=self._obtain) 
        if not self._refresh is  None:  
            self._api.add_resource(resource_name=self._refresh)
        if not self._verify is None:        
            self._api.add_resource(resource_name=self._verify)   
        self._token = None  
        self._status = None
        self._error = None  

    @property
    def token(self):
        return self._token

    @property
    def status(self):
        return self._status

    @property
    def error(self):
        return self._error    

    def _request(self,resource_name,data):
        self._token = None  
        self._status = None
        self._error = None          
        body = None
        response = None
        res = getattr(self._api,resource_name)
        try:
            response = res.create(body=data)
        except Exception as e :
            if isinstance(e,exceptions.ClientConnectionError):
                self._error = {'client_connections_error':[_('connection error.')]}
            elif isinstance(e,exceptions.ActionNotFound):       
                self._error = {'ation_not_found_error':[_('action not found.')]}
            elif isinstance(e,exceptions.ActionURLMatchError):
                self._error = {'ation_url_match_error':[_('action URL match error.')]}
            elif isinstance(e,exceptions.ErrorWithResponse):     
                response = getattr(e,'response',None)
                self._error = getattr(response,'body',None)
        if not response is None:
            self._status = response.status_code 
            body = response.body      
        return body              

    def obtain(self,username,password):
        data ={
            'username': username,
            'password': password,
        }
        body = self._request(self._obtain,data)
        if body:
            self._token = body.get('token',None)
        return  self._token   

    def refresh(self,token=None):
        data = {
            'token':token
        }
        body = self._request(self._refresh,data)
        print(body)
        if body:
            self._token = body.get('token',None)
        return  self._token               

    def verify(self,token=None):
        data = {
            'token':token
        }
        body = self._request(self._verify,data)
        if body:
            print(body)        

        


class ClientJwt():
    ''' 微服务客户端
    '''
    def __init__(self,service_name,options=None,auth=None):
        self._options = options or  getattr(djms_settings,'CLIENT')
        self._service_name = service_name
        self._url = default_discover.get_url(service_name)
        if isinstance(auth,AuthJwt):
            self._auth = auth
        else:
            self._auth = AuthJwt(
                default_discover.get_url(self._options.get('AUTH')),
                self._options.get('OBTAIN'),
                self._options.get('REFRESH'),
                self._options.get('VERIFY'),
                self._options.get('TIMEOUT')
            )
        self._api = API(api_root_url=self._url,
                        json_encode_body=True,
                        headers={'Content-Type': 'application/json'},
                        append_slash=True,
                        timeout = self._options.get('TIMEOUT')
                        )  

        self._status = None
        self._error = None

    @property
    def status(self):
        return self._status

    @property
    def error(self):
        return self._error                 

    def login(self,username=None,password=None):
        """ 登陆
        """
        username = username or self._options.get('USER')
        password = password or self._options.get('PASSWORD')
        return self._auth.obtain(username,password)

    def _create_jwt_header(self):
        """ 创建JWT头部
        """
        header = {}
        if self._auth.token:
            header['Authorization'] = "%s %s"%(self._options.get('JWT_HEADER_PFX'),self._auth.token)
        return header    

    def action(self,resource,action='list',id=None,body=None,params=None,headers=None):
        """ 执行操作
        """
        self._status = None
        self._error = None
        res = getattr(self._api,resource,None)
        if res is None:
            self._api.add_resource(resource_name=resource)
            res = getattr(self._api,resource) 

        act = getattr(res,action)
        headers = headers or {}
        response = None
        data = None
        auto_login = self._options.get('AUTO_LOGIN',False)

        while True:
            if self._auth.token is None and auto_login:
                self.login(
                    self._options.get('USER'),
                    self._options.get('PASSWORD')
                )
                if self._auth.token is None:
                    break

            headers.update(self._create_jwt_header())

            try:
                response = act(id,body=body,headers=headers,params=params)
            except Exception as e :
                if isinstance(e,exceptions.ClientConnectionError):
                    self._error = {'client_connections_error':[_('connection error.')]}
                elif isinstance(e,exceptions.ActionNotFound):       
                    self._error = {'ation_not_found_error':[_('action not found.')]}
                elif isinstance(e,exceptions.ActionURLMatchError):
                    self._error = {'ation_url_match_error':[_('action URL match error.')]}
                elif isinstance(e,exceptions.ErrorWithResponse):     
                    response = getattr(e,'response',None)
                    self._error = getattr(response,'body',None)
            if not response is None:
                self._status = response.status_code 
                data = response.body   

            if self.status == 401 and auto_login:
                self._auth._token = None    
            else:
                break    

        return data              

