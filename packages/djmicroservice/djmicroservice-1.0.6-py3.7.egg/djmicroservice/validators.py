from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible

validator_perm_type = RegexValidator(
    regex=r'^operation|object$',
    message=_("权限类型只能是:'operation'|'object'."))

validator_phone_number = RegexValidator(
    regex=r'^[0-9\+\-]{7,24}$',
    message=_("电话号码是7-24个'0-9+-'字符."))

@deconstructible
class StringListValidator():
    '''验证字符分隔的字符串列表
    '''
    def __init__(self,seq = ',',string_list = None,length = 0,message = None):
        if not type(string_list) in (type(None),list,tuple):
            raise ValueError(_('`string_list`必需是一个list或tuple对象') )
        self._seq = seq or ','
        self._string_list = string_list or []
        self._length = length or 0
        strlist = '|'.join(self._string_list)
        strlen = length if length > 0  else '不限'
        message = message or _('字符串必需是`%(seq)s`分隔,子字符串必需是%(list)s之一,长度%(length)s.')
        self._error = ValidationError(
            message,
            params={
                'seq': seq,
                'list': strlist,
                'length': strlen
            }
        )

    def __call__(self,value):
        if not isinstance(value,str):
            raise self._error
        substrs = value.split(self._seq)
        for substr in substrs:
            if not substr in self._string_list:
                raise self._error

        if self._length > 0 and len(substrs) != self._length:
            raise self._error
            
