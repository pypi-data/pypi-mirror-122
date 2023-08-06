from django.apps import apps
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from .permissions import RolePermission

class RolePermViewsetMixin():
    '''角色权限混合类,用于在ViewSet中混入基于角色的权限控制
        
        ```
        class AccountViewSet(RolePermViewsetMixin,viewsets.ModelViewSet):
            role_permissions = {
                'list':('onlyuser.user.list','Can query user lsit',''),
                ....
            }
            pass
        ```
    '''
    def __init__(self,*args,**kwargs):
        if hasattr(self,'permission_classes') and not ( RolePermission in self.permission_classes):
            self.permission_classes = self.permission_classes + (RolePermission,)
        else:
            self.permission_classes = (RolePermission,)
        
        if not hasattr(self,'service_name'):
            mssettings = __import__('djmicroservice.settings',fromlist=['djms_settings'])
            print(mssettings)
            if mssettings and hasattr(mssettings,'djms_settings'):
                self.service_name = mssettings.djms_settings.NAME
            else:    
                appcfg = apps.get_containing_app_config(self.__class__.__module__)
                if appcfg and hasattr(appcfg,'name'):
                    self.service_name = appcfg.name.lower()
                else:
                    raise APIException(detail='RolePermViewsetMixin needs to set class attribute service_name.')
        
        if not hasattr(self,'resource_name'):
            view_name = self.__class__.__name__
            self.resource_name = view_name.replace('ViewSet','').lower()+'s'
             
        if not hasattr(self,'role_permissions') or not isinstance(self.role_permissions,dict):
            self.role_permissions = {}
            
        if isinstance(self,ModelViewSet):
            default_actions = ('list','retrieve','create','update','partial_update','destroy')
            for action in default_actions:
                if hasattr(self,action) and not action in self.role_permissions:
                    code = "%s.%s.%s"%(self.service_name,self.resource_name,action)
                    name = "Can %s %s's %s"%(action,self.service_name,self.resource_name)
                    self.role_permissions.__setitem__(action,(code,name,name))
                    
        if not hasattr(self,'object_permissions') or  not isinstance(self.role_permissions,list):
            self.object_permissions = []
            
        if isinstance(self,ModelViewSet):
            sets = ('own','group','branch','organize','all')
            operations = ('see','update','destroy')
            for s in  sets:
                for op in operations:
                    code = "%s.%s.%s.%s"%(self.service_name,self.resource_name,s,op)
                    name = "The ability to %s the %s.%s object of %s"%(op,self.service_name,self.resource_name,s)
                    self.object_permissions.append((code,name,name))                
                    
        super().__init__(*args,**kwargs)
        
        
    def get_role_permissions(self):
        return list(self.role_permissions.values())
        
    def get_role_permission_code(self,action=None):
        if action is None:
            action = self.action
        if  action in  self.role_permissions:
            return self.role_permissions.get(action)[0]            
        return "%s.%s.%s"%(self.service_name,self.resource_name,action)
 
    def get_object_permissions(self):
        return self.object_permissions