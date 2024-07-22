# demoapp/views.py
import os
import logging
import json
import importlib
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from framework.common.exception import APIException

logger = logging.getLogger('DemoAppService')

@csrf_exempt
def index(request):
    if request.method == 'POST':
        logger.info('New POST Request')
        data = json.loads(request.body)
        action = data.get('Action')
        try:
            handler_module = importlib.import_module(f'apps.demoapp.handlers.{action}')
            return handler_module.handle(data)
        except ModuleNotFoundError:
            raise APIException()
    elif request.method == 'GET':
        logger.info('New GET Request')
    else:
        logger.info('unknow http line')
    return HttpResponse('')
