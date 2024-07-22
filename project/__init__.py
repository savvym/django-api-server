from .celery import app as celery_app
import bussiness

bussiness.mount()

__all__ = ('celery_app',)
