from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


__all__ = ['SummaryRelatedField']

class SummaryRelatedField(serializers.RelatedField):
    """
    显示摘要信息, 可读写, 通过ID字段关联到目标, 参数fields指示返回的字段
    """

    def __init__(self, fields=None, **kwargs):
        self.fields = fields or []
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(id=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', value=data)
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        result = {'id':obj.id}
        for field in self.fields:
            result[field] = getattr(obj, field)
        return result

class HideCharField(serializers.CharField):
    '''可以部分隐藏的字符串字段
       初如化参数除了标准字符串字段的参数外,有以下专用参数:
       @fill_char     填充隐藏位置的字符
       @hide_start    隐藏开始位置,从0开始
       @hdie_end      隐藏结束位置,如果是-1则表示到结尾
    '''
    def __init__(self, *args, **kwargs):
        self._fill_char = kwargs.get('fill_char', '*')
        self._hide_start = kwargs.get('hide_start', 0)
        self._hide_end = kwargs.get('hide_end', -1)
        kw = kwargs
        if 'fill_char' in kw:
             kw.pop('fill_char') 
        if 'hide_start' in kw:
            kw.pop('hide_start') 
        if 'hide_end' in kw:
            kw.pop('hide_end') 
        super().__init__(*args, **kwargs) 

    def to_representation(self, value):
        data = super().to_representation(value)

        if self._hide_end<0:
            hide_str = data[self._hide_start:]
        else:
            hide_str = data[self._hide_start:self._hide_end]
        
        hide_len = len(hide_str)
        return data[:self._hide_start] + self._fill_char*hide_len + data[self._hide_start+hide_len:]