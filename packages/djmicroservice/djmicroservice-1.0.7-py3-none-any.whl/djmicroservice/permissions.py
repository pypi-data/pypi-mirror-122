'''角色权限控制
'''
from rest_framework import permissions

class RolePermission(permissions.BasePermission):
    '''基于角色的权限控制        
    '''
    def has_permission(self, request, view):
        ''' 检查权限
        '''
        user = models.User.objects.get(username=request.user)
        #if user.is_admin:
        #    return True
            
        perm_code = view.get_role_permission_code() 
        print(perm_code)
        print(user.id)
        print(user.is_admin)
        print(user.roles)
        return True
        
        
    def has_object_permission(self, request, view, obj): 
        perm_code = view.get_role_permission_code() 
        print(perm_code)
        return True