# coding:utf-8
# 上下文与缓存抽象
import sys
from .static import _tls


class Context(object):
    """
        请求级别上下文
        协议要求：
            * 实现 in 操作符
            * get 方法
            * 动态获取设置属性
            * 重载 [] 运算符，支持获取与设置
    """

    def __contains__(self, name):
        return name in _tls.context

    def __call__(self):
        self.__dict__ = {}

    def get(self, name, default=None):
        if name == '__wrapped__':
            return False
        try:
            return _tls.context[name]
        except KeyError:
            return default

    def __init__(self):
        pass

    def __getitem__(self, name):
        return _tls.context[name]

    def __getattr__(self, name):
        if name == '__wrapped__':
            return
        return _tls.context[name]

    def __setitem__(self, name, val):
        _tls.context[name] = val

    def __setattr__(self, name, val):
        _tls.context[name] = val

    def keys(self):
        return _tls.context.keys()


try:
    sys.modules['context'] = Context()
except:
    pass
try:
    sys.modules['framework.context'] = Context()
except:
    pass
