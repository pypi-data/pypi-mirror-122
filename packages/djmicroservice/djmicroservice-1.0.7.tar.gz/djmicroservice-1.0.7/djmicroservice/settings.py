""" 微服务配置
"""
import os
from django.conf import settings
from rest_framework.settings import APISettings

user_settings = getattr(settings,'DJMICROSERVICE',None)

# 微服务默认名字
DEFAULT_NAME = os.environ['DJANGO_SETTINGS_MODULE'].split('.')[0]

default_settings = {
    # 微服务名字
    'NAME': DEFAULT_NAME ,
    # 微服务URL
    'URL': 'http://127.0.0.1:8000/',
    # 是否是主节点
    'MASTER': True, 
    # 微服务资源
    'RESOURCES': {        
    }, 
    # 服务发现配置 
    'DISCOVER': {
        # 是否注册
        'REGISTER': False,
        # 心跳
        'HEARTBEAT': 15,
        # 发现者引擎 
        'ENGINE': 'djmicroservice.discovers.backends.StaticDiscover',
        # 引擎配置
        'OPTIONS': {
            'SERVICES':[
            ]
        },
  
    },

    #客户端配置
    'CLIENT':{        
        # 认证管理微服务名
        'AUTH': None,
        'OBTAIN': None,
        'REFRESH': None,
        'VERIFY': None,
        'USER': None,
        'PASSWORD': None,
        'JWT_HEADER_PFX': 'JWT',
        'TIMEOUT': 2,
        'AUTO_LOGIN': False,
    },  

    #消息队列端配置  
    'MQ':{
        #消息队列引擎
        'ENGINE': 'djmicroservice.mq.backends.ActiveMQ',
        #引擎配置
        'OPTIONS': {
            #消息服务器地址,可以多个
            'SERVERS': [('127.0.0.1',61613)],
            #消息服务器登录名
            'USER': 'admin',
            #消息服务器密码
            'PASSWORD': 'admin',
        },
        'HANDLERS': { 
        },
        
    },
    'SERVICE_MANAGER':{
        #服务管理地址
        'BIND':('127.0.0.1',56560),
        'AUTHKEY':None,
        #要启动的服务
        'SERVICES':[        
            #{
            #    'CLASS': 'onlyuser.mq.service.MQService', 
            #    'COUNT': 1,
            #    'OPTIONS': None
            #},
        ]
    }
} 


djms_settings = APISettings(user_settings,default_settings,None)