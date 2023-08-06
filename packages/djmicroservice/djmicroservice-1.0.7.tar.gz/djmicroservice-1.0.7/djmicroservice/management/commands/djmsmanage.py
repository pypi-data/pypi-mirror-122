from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from user.models import User,Role,Permission,Group,Organization
from djmicroservice.settings import djms_settings
from djmicroservice import signals
from djmicroservice.utils import import_object
from djmicroservice.discovers import default_discover

class Command(BaseCommand):
    help = "Micro service manage command."

    def add_arguments(self, parser):
        parser.add_argument('-I'
                            '--install',
                            action='store_true',
                            dest='install' , 
                            help='Install micro service.')

        parser.add_argument('-U'
                            '--upgrade',
                            action='store_true',
                            dest='install' , 
                            help='Upgrade micro service.')   

        parser.add_argument('-R'
                            '--register',
                            action='store_true',
                            dest='register' , 
                            help='Register micro service.') 


    def _migrate(self):
        ''' 数据迁移
        '''
        call_command('makemigrations')
        call_command('migrate')

    def _install_monitor(self):
        ''' 安装微服务监控器
        '''
        pass    


    def _install(self):
        ''' 安装微服务
        '''
        self._migrate()
        self._install_monitor()
        self._register()
        signals.post_install.send(self.__class__,djms_settings=djms_settings)

    def _upgrade(self):
        ''' 升级
        '''
        self._migrate()
        self._register()
        signals.post_upgrade.send(self.__class__,djms_settings=djms_settings)



    def _update_perms(self,service,resource,viewset):
        ''' 更新权限数据
        '''
        v = import_object(viewset)()
        perms = v.get_role_permissions()
        operms = v.get_object_permissions()
        print(perms,operms)
        pass    


    def _register(self):
        ''' 注册微服务
        '''
        resources = getattr(djms_settings,'RESOURCES',None) 
        service_name = getattr(djms_settings,'NAME',None)
        service_url = getattr(djms_settings,'URL',None)   
        default_discover.register(service_name,service_url)
        for resource_name,viewset in resources.items():
            self._update_perms(service_name,resource_name,viewset)
        signals.post_register.send(self.__class__,djms_settings=djms_settings)  

    def handle(self, *args, **options):
        if options.get('install',False):
            self._install()
        elif options.get('upgrade',False):
            self._upgrade()
        elif options.get('register',False):
            self._register()

