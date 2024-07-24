import logging

from pydantic import BaseModel, Field

from framework.router import action, schema
from framework.static import get_current_request_id
from framework import context

logger = logging.getLogger('django')


class AddReqeustModel(BaseModel):
    Action: str = Field(description="An string parameter")
    Args: list = Field(description="A list parameter", default=list())


@action(desc='Add加法接口')
@schema.request(validator = AddReqeustModel)
@schema.response()
def entry(**args):
    logger.info('start add')
    request_id = get_current_request_id()
    ret = {
        'msg': 'this is a add',
    }
    return ret

