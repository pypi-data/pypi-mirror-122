import math
from django.db import models
from django.db.models import Q
from rest_framework import serializers
from .utils import ObjectID
from .utils import  create_objectid as _create_objectid 

class ObjectidModel(models.Model):
    '''objectid ID model
    '''
    id = models.CharField('id',max_length=24,primary_key=True,default=_create_objectid)

    def get_id_datetime(self):
        oid = ObjectID(self.id)
        return oid.timestamp

    class Meta:
        abstract = True


class TreeManager(models.Manager):
    '''树状结构管理类
    '''
    def __init__(self,parent_field=None,key_field=None,max_depth=10):
        '''构造方法
           @parent_field   父节点指针字段名
           @key_field      key字段名
        '''
        super().__init__()
        self._parent_field = parent_field or 'parent'
        self._key_field = key_field or 'key'
        self._max_depth = max_depth


    def _get_parent_field(self):
        '''返回父节点指针字段名
        '''
        if self._parent_field is not None and hasattr(self.model,self._parent_field):
            return self._parent_field
        elif hasattr(self.model,'parent'):
            return 'parent'
        raise AttributeError('模型类必须包含`parent`字段,或者在实例化时有命名参数`parent_field`指定')    


    def _get_key_field(self):
        '''返回key字段名
        '''        
        if self._key_field is not None and hasattr(self.model,self._key_field):
            return self._key_field
        elif hasattr(self.model,'key'):
            return 'key'
        raise AttributeError('模型类必须包含`key`字段,或者在实例化时有命名参数`key_field`指定')    


    def get_parent_node(self,node):
        '''返回节点的父节点对象
           @node 节点实例
        '''
        if node is None:
            raise ValueError('`node`不能是None')        
        parent_field = self._get_parent_field()
        return getattr(node,parent_field)


    def get_key_value(self,node):
        '''返回节点的key字段值
           @node 节点实例
        '''
        if node is None:
            raise ValueError('`node`不能是None')        
        key_field = self._get_key_field()
        return getattr(node,key_field)


    def get_node_depth(self,node):
        '''获取节点深度度
           @node 节点实例
        '''
        key = self.get_key_value(node)    
        key_len = len(key)
        dec,depth = math.modf(key_len/24)
        if dec>0:
            raise ValueError("`%s`的key值无效:%s"%(node,key))
        return depth+1    


    def create_node(self,parent=None,**extra_fields):
        '''新建节点
           @parent       父节点
           @extra_fields 其他字段 
        ''' 
        parent_field = self._get_parent_field()
        key_field = self._get_key_field()
        extra_fields[parent_field] = parent
        if key_field in extra_fields:
            extra_fields.pop(key_field)
        key = ''
        if not parent is None:
            if self.get_node_depth(parent)>=self._max_depth:
                raise ValueError("树结构允许最大深度%d"%(self._max_depth))
            key = self.get_key_value(parent)+parent.pk
        extra_fields[key_field] = key   
        node = self.create(**extra_fields)    
        node.save()
        return node      


    def get_childs(self,node):
        '''获取节点的子节点
           @node  节点对象 
        '''
        if not node:
            raise ValueError("`node`必须设置")
        parent_field = self._get_parent_field()    
        #child_key= node.key + node.pk
        params={parent_field: node.pk}
        qset = self.model.objects.filter(**params)
        return qset                    

    def rebuild_key(self,node):
        '''重建节点及子节点的key
        '''
        key = ''
        parent = self.get_parent_node(node)
        key_field = self._get_key_field()
        if parent: 
            key =self.get_key_value(parent) + parent.pk     
        setattr(node, key_field, key)
        node.save()                   
        childs = self.get_childs(node)
        for child in childs:
            self.rebuild_key(child)


    def change_parent(self,node,parent=None):
        '''改变节点的父节点
           @node   节点对象
           @parent 父节点对象 
        '''
        if not node:
            raise ValueError("`node`必须设置") 
        parent_field = self._get_parent_field()

        if parent:
            if parent.pk == node.pk:
                raise ValueError("父节点不能指向自己")
            childs = self.get_childs(node)
            if childs.filter(pk = parent.pk).exists():
                raise ValueError("新的父节点是此节点的子节点")
            if self.get_node_depth(parent)>=self._max_depth:
                raise ValueError("树结构允许最大深度%d"%(self._max_depth))
        setattr(node, parent_field, parent)    
        node.save()
        self.rebuild_key(node)
        return node             


    def generate_serializer_data(self,root):
        '''生成序列化数据
           @root 准备序列化树的根节点
        '''
        class TheModelSerializer(serializers.ModelSerializer):
            class Meta:
                model = self.model
                fields = ('__all__')

        def generate(root):
            serializer = TheModelSerializer(root)
            data = serializer.data
            data['childs'] = []
            for child in self.get_childs(root):
                child_data = generate(child)
                data['childs'].append(child_data)
            return data

        return generate(root)


    def get_root_all(self):
        '''返回全部根节点
        '''
        key_field = self._get_key_field()    
        params={key_field:''}
        qset = self.model.objects.filter(**params)  
        return qset      


    def find_node_root(self, node):
        '''查找节点的根节点
           @node 节点对象
        '''
        key = self.get_key_value(node)
        if key=='':
            return node
        if not self.model.objects.filter(pk=key[:24]).exists():
            raise ValueError("`%s`的key值无效:%s"%(node,key))
        return self.model.objects.get(pk=key[:24])    

    def siblings(self, node):
        '''返回节点的同胞节点
           @node 节点对象
        '''
        key = self.get_key_value(node)
        key_field = self._get_key_field()    
        params={key_field:key}
        qset = self.model.objects.filter(Q(**params) & ~Q(pk=node.pk))  
        return qset        

    def remove(self, node, remove_childs = True):
        '''删除对象
           @node 节点对象
           @childs 删除子节点
        '''
        childs = self.get_childs(node)
        if remove_childs:            
            for child in childs:
                self.remove(child, True)
        else:
            parent = self.get_parent_node(node)
            for child in childs:
                self.change_parent(child,parent)        
        node.delete()    

