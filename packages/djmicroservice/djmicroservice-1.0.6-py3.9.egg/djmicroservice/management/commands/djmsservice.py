'''后台服务进程管理命令
'''
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from djmicroservice.settings import djms_settings
from djmicroservice.service.manager import ServiceManager

class Command(BaseCommand):
    help = "Micro service background service manage."

    def add_arguments(self, parser):
        parser.add_argument('-f',
                            '--foce',
                            action='store_true',
                            dest='foce' , 
                            help='Foce execute command.')

        parser.add_argument('command',
                            action='store',
                            choices=['start','stop','restart'],
                            help='Command.')

        parser.add_argument('service',
                            action='store',
                            nargs='?',
                            help='Background service name.')

    def handle(self, *args, **options):
        cmd = options.get('command')
        service = options.get('service')
        foce = options.get('force')
        conf = getattr(djms_settings,'SERVICE_MANAGER',None)
        manager = ServiceManager(conf)
        daemon_runing = not manager.get_status() is None
        if service is None:
            #全局命令
            if cmd == 'start':
                if  not daemon_runing:
                    manager.start_server()
        else:
            
            pass  