# middlewares.py
import logging
import uuid
import json

from django.http.response import JsonResponse
from django.http import HttpResponseServerError
from django.middleware.common import MiddlewareMixin

from framework import context
from framework.static import _tls
from framework.common.exception import APIException

logger = logging.getLogger('django')

class ThreadLocalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _tls.request = request  # 设置线程本地数据
        _tls.request_id = str(uuid.uuid4())
        response = self.get_response(request)
        return response
    

class ProcessMiddleware(MiddlewareMixin):
    def process_request(self, request):
        data = json.loads(request.body)
        context.Action = data.get('Action') 

    def process_response(self, request, response):
        return response

    """统一异常处理中间件"""

    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求对象
        :param exception: 异常对象
        :return:
        """
        if isinstance(exception, APIException):
            data = {
                'code': exception.icode,
                'msg': exception.message,
                'errMsg': exception.code
            }
            return JsonResponse(data)
        elif isinstance(exception, Exception):
            # 服务器异常处理
            logger.error(exception, exc_info=True)
            return HttpResponseServerError()
        return None


