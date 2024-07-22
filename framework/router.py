import logging

from pydantic import ValidationError
from framework.common import exception

logger = logging.getLogger('django')

# 定义一个全局的路由器
router = {}
supported_actions = {}

def get_inquiry_price_action_name_prefix():
    return 'InquiryPrice'


def get_switch_parameter_action_name_prefix():
    return 'SwitchParameter'


def get_validator_action_name_prefix():
    return 'Validate'


def get_checkoffering_action_name():
    return 'DescribeInstancesOfferings'


def action(url='http://api.qcloud.com/v2', inquiryable=False, switchable=False, validateable=False,
           checkofferingable=False, **args):
    def _(func):
        assert func.__name__ == 'entry', "API 入口必须以 entry 作为函数名，而不能是 %s。" % func.__name__
        supported_actions[func.name] = func   # func.name 就是接口的 Action
        if inquiryable:
            supported_actions[get_inquiry_price_action_name_prefix() + func.name] = func
        if switchable:
            supported_actions[get_switch_parameter_action_name_prefix() + func.name] = func
        if validateable:
            supported_actions[get_validator_action_name_prefix() + func.name] = func
        if checkofferingable:
            supported_actions[get_checkoffering_action_name()] = func
        assert 'recv' in dir(func), "%s API 没有使用 recv 来修饰入参。" % func.name
        assert 'send' in dir(func), "%s API 没有使用 send 来修饰入参。" % func.name
        func.url = url
        assert args.get('desc'), "%s API 没有为 Action 增加描述。" % func.name
        func.desc = args['desc']
        logging.debug('识别到 %s 入口点并挂载...' % func.name)

        return func

    return _

class Router(object):
    """
    API路由类
        将请求分发到各个业务的 Action 处理器。
    >>> api = Router();api.send({'action': 'ff'});print(api.recv());
    Traceback (most recent call last):
        ...
    framework.prototype.exception.MissingAction: The request is missing an action.
    >>> api = Router();api.send({'Action': 'Run'});print(api.recv());
    Traceback (most recent call last):
        ...
    framework.prototype.exception.InvalidParameterValue: The value Run specified in the parameter Action is not valid.
    """

    def reg(self, action_name, action_func):
        supported_actions[action_name] = action_func

    def __init__(self):
        pass

    def parse_action_name_from_data(self, data):
        if 'Action' not in data:
            raise exception.MissingAction()

        return data['Action']

    def send(self, data):
        action_name = self.parse_action_name_from_data(data)
        action = self.get_next_action(action_name)
        self.data = action(**data)

    def recv(self):
        return self.data

    @classmethod
    def get_next_action(cls, action_name):
        if action_name not in supported_actions:
            logger.debug(supported_actions.keys())
            raise exception.InvalidParameterValue(parameter='Action', value=action_name)

        return supported_actions[action_name]


class schema(object):

    @staticmethod
    def request(**args):
        def _(func):
            # 获取接口 func name
            source_file_path_elem = func.raw_func.__code__.co_filename.split(
                '/')
            if 'name' not in args:
                name = source_file_path_elem[-1].split('.')[0]
            else:
                if '.' in args['name']:
                    args['name'] = args['name'].split('.')[-1]
                name = args['name']
            # 使用 pydantic 校验参数
            validator = None
            if 'validator' in args:
                validator = args['validator']

            def wrap_func(**input_args):
                try:
                    if validator:
                        validator(**input_args)
                except ValidationError as e:
                    raise exception.APIException()
                    # raise exception.BusinessException(message = str(e))
                except Exception as e:
                    raise exception.InternalError(str(e))
                result = func(**input_args)
                return result   
                
            wrap_func.__doc__ = func.__doc__
            wrap_func.__name__ = func.__name__
            wrap_func.raw_func = func.raw_func
            wrap_func.recv = args
            wrap_func.send = func.send

            wrap_func.name = name

            return wrap_func

        return _


    @staticmethod
    def response(**args):
        def _(func):

            def wrap_func(**input_args):
                result = func(**input_args)
                return result

            wrap_func.__doc__ = func.__doc__
            wrap_func.__name__ = func.__name__
            wrap_func.raw_func = func
            wrap_func.send = args
            return wrap_func
        return _
