import time
from queue import Queue
from multiprocessing import Process
from multiprocessing.managers import BaseManager
from .base import  BaseService
from djmicroservice.utils import import_object

#默认服务管理进程通信地址
DEFAULT_SERVICE_MANAGER_ADDR = ('127.0.0.1',56560)
#默认通信密钥
#DEFAULT_AUTHKEY = b'0\xca\xc4/q{\xa3Q\x8b\xf9\x93\xba\x14\x01on+(C2)\xe1iB\xba\x1f\xa5\xb6}\xf1\xedH'
DEFAULT_AUTHKEY = b'1234'

#控制命令
COMMAND_DAEMON_EXIT = 'DAEMON_EXIT'
COMMAND_DAEMON_FORC_EXIT = 'DAEMON_FORC_EXIT'
COMMAND_SERVICE_FORC_STOP = 'SERVICE_FORC_STOP'
COMMAND_SERVICE_STOP = 'SERVICE_STOP'
COMMAND_SERVICE_RESTART = 'SERVICE_RESTART'


class ServiceMonitor():
    '''后台服务监控
    '''
    

#服务进程函数
def service_process(srvobj):
    if not isinstance(srvobj,BaseService):
        return 
    srvobj.start()    


#服务控制    
ctrlqueue = Queue()
#服务状态    
status = []

def get_ctrlqueue():
    global ctrlqueue
    return ctrlqueue

def get_status():
    global status
    return status    

#服务管理守护进程
def service_daemon(services,bind=None,authkey=None): 
    print('The djmicroservice service manager starting.')
    bind = bind or  DEFAULT_SERVICE_MANAGER_ADDR
    authkey = authkey or DEFAULT_AUTHKEY 
    #远程共享管理类
    class ShareManager(BaseManager):pass  
    #服务控制    
    global ctrlqueue 
    #服务状态    
    global status 
    #服务对象
    srvobjs = []
    #进程对象
    procs = []
    print(bind,authkey)
    ShareManager.register('get_ctrlqueue', callable=lambda:ctrlqueue)    
    ShareManager.register('get_status', callable=lambda:status) 
    m = ShareManager(address=bind, authkey=authkey)
    m.start()
    #srv = m.get_server()
    #srv.serve_forever()
    
    time.sleep(3)
    return 
    for item in services:
        clsname = item.get('CLASS',None)
        if clsname is None:
            continue
        cls = import_object(clsname)
        if not issubclass(cls,BaseService):
            continue

        count = item.get('COUNT',1)
        options = item.get('OPTIONS',None)
        for i in range(count):
            obj = cls(options)
            srvobjs[i] = obj                     
            proc = Process(target=service_process,args=(obj,))
            procs[i] = proc
            proc.start()
            status[i] = [obj.name,obj.is_runing(),time.time()]    
    #m.shutdown()         
    #return 
    while True:
        print('deamon process runing.')
        try:
            evt = ctrlqueue.get(True,timeout=0.5)
        except:
            continue    
        if not isinstance(evt,dict):
            continue
        cmd = evt.get('command',None)
        options = evt.get('options',None)
        if cmd ==  COMMAND_DAEMON_EXIT:                
            for srv in srvobjs:
                srv.stop()
            #等待所有服务进程退出    
            all_stop = False
            while not all_stop:
                for srv in srvobjs:
                    if srv.is_runing():
                        all_stop = False
                        break
                time.sleep(0.5)
            break

        elif cmd == COMMAND_DAEMON_FORC_EXIT:
            for proc in procs:
                proc.terminate()
            break    

        elif cmd == COMMAND_SERVICE_FORC_STOP:    
            srvname = options.get('NAME',None)
            if not srvname is None:
                for srv in srvobjs:
                    if srv.name == srvname:
                        i = srvobjs.index(srv)
                        procs[i].terminate()
                        break

        elif cmd == COMMAND_SERVICE_STOP:
            srvname = options.get('NAME',None)
            if not srvname is None:
                for srv in srvobjs:
                    if srv.name == srvname:
                        srv.stop()
                        break

        elif cmd == COMMAND_SERVICE_RESTART:
            srvname = options.get('NAME',None)
            if not srvname is None:
                for srv in srvobjs:
                    if srv.name == srvname:
                        srv.restart()
                        break

        #更新服务进程状态                
        for srv in srvobjs:
            i = srvobjs.index(srv)
            status[i][1] = srv.is_runing()


class ServiceManager():
    """后台服务管理类
    """
    def __init__(self,settings=None):
        settings = settings or {}
        self._bind = settings.get('BIND',DEFAULT_SERVICE_MANAGER_ADDR)        
        self._authkey = settings.get('AUTHKEY',DEFAULT_AUTHKEY)
        self._services = settings.get('SERVICES',[])
        class ShareManager(BaseManager):pass  
        ShareManager.register('get_ctrlqueue')    
        ShareManager.register('get_status') 
        self._sharemanager = ShareManager(address=self._bind, authkey=self._authkey)            

    def send_ctrl(self,cmd,options=None):
        try:
            self._sharemanager.connect()
        except Exception as e:
            return False
        cq = self._sharemanager.get_ctrlqueue()
        evt = {
            'command': cmd,
            'options': options
        } 
        cq.put(evt) 
        return True          

    def start_server(self):
        #srv = Process(target=service_daemon,args=(self._services,self._bind,self._authkey))
        service_daemon(self._services,self._bind,self._authkey)
        #srv.start()
        #srv.join()
        #srv.close()

    def stop_server(self,forc=False):
        cmd = COMMAND_DAEMON_EXIT
        if forc:
            cmd = COMMAND_DAEMON_FORC_EXIT
        return self.send_ctrl(cmd)
        

    def stop_service(self,name,forc=False):
        if name is None:
            return
        cmd = COMMAND_SERVICE_STOP
        if forc:
            cmd = COMMAND_SERVICE_FORC_STOP
        return self.send_ctrl(cmd,{'name':name})

    def restart_service(self,name):
        if name is None:
            return
        cmd = COMMAND_SERVICE_RESTART
        return self.send_ctrl(cmd,{'name':name})            

    def get_status(self,name=None):
        try:
            self._sharemanager.connect()
        except:
            return None    
        status = self._sharemanager.get_status()   

        if not isinstance(name,str):
            return status

        stat = []       
        for st in status:
            if st[0] == name:
                stat.append(st)
        return stat        


            