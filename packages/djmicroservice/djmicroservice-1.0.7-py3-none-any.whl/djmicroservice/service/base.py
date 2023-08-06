import time
class BaseService():
    """后台服务基类 
    """
    name = "BaseService"
    def __init__(self,options=None):
        self._options = options or {}
        #服务是否运行
        self._runing = False
        #控制标志 0:等待,1:停止,2:重启
        self._ctrl = 0
        #服务启动时间
        self._start_time = 0

    def start(self):
        """启动服务
        """
        if self._runing:
            return 0
        while True:
            self._runing = True            
            self._start_time = time.time()                        
            exit_code = self.run(self._options)
            self._runing = False 
            if self._ctrl != 2:                
                break
            self._ctrl = 0 
        self._ctrl = 0    
        return exit_code   
               

    def stop(self):
        """停止
        """
        if self._runing:
            self._ctrl = 1


    def restart(self):
        """重启
        """
        if self._runing:
            self._ctrl = 2

    def is_runing(self):
        """是否运行中
        """
        return self._runing

    def run(self,options=None):
        pass

    @property
    def ctrl(self):
        return self._ctrl

