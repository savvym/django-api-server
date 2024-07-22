from django.http import JsonResponse
from project import celery_app as app

def handle(data):
    res = {'message': 'Handle Add', 'data': data}
    return JsonResponse(res)