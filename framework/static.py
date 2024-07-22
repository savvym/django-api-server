# 进程的静态存储区：用来提供具有进程级生命周期的变量。
# 实现 context 功能依赖 static 所提供的能力。
# 使用static定义可变变量（例如list,map）时，注意清理数据，否则会造成内存泄漏。
import threading


class _TLS(threading.local):
    request = None
    request_id = None
    context = {}


_tls = _TLS()

def get_current_request():
    return _tls.request

def get_current_request_id():
    return _tls.request_id

