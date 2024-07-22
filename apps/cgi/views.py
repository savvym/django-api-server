import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from framework.router import Router
from framework.common import exception
# Create your views here.



@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        api = Router()
        api.send(data)
        result = JsonResponse(api.recv())
        return result
    else:
        exception.UnknownAPIRequest()