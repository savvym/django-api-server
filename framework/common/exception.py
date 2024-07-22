# exceptions.py
import logging

from framework import context

logger = logging.getLogger('django')

EXCEPTION_MESSAGE_MAP = {
    'UnknownAPIRequest': 'The request is not recognized.',
    'UnknownParameter': 'The parameter `%(name)s` is not recognized.',
    'ResourceNotFound': 'Resource `%(resource)s` not found.',
    'InvalidParameter': 'A parameter `%(parameter)s` specified in a request is '
                          'not valid.',
    'InvalidParameter.FormatError': 'A parameter `%(parameter)s` format error',
    'InvalidParameterValue': 'The value `%(value)s` specified in the parameter '
                               '`%(parameter)s` is not valid.',
    'InvalidParameterValue.Range': 'The value `%(value)s` specified in the parameter '
                                     '`%(parameter)s` is out of range.',
    'InvalidParameterValue.Length': 'The length `%(value)s` specified in the parameter '
                                      '`%(parameter)s` must between [%(min)s, %(max)s].',
    'InternalServerError': 'Internal Server Error.',
    'InternalError': 'An internal error has occurred. Retry your request, but if the problem persists, contact us with details by posting a message on the Tencent cloud forums.',
    'MissingParameter': 'Lack of parameter `%(parameter)s`.',

    'InvalidFilter': 'The specified filter `%(value)s` is not valid.',
    'InvalidFilterNotDict': 'The specified filter `%(value)s` is not a key value dictionary.',
    'InvalidFilterInvalidKey': 'The specified filter `%(value)s` does not exist and only exists the `Name` and `Values` keys.',
    'InvalidFilterInvalidNameNotStr': 'The specified filter Name `%(value)s` is not a string.',
    'InvalidFilterInvalidValuesNotList': 'The specified filter Name `%(name)s` Values `%(value)s` is not a list.',
    'InvalidFilterNotSupportedName': 'The specified filter Name `%(value)s` is not supported.',
    'InvalidFilterValueLimitExceeded': 'The request uses too many filter Name `%(name)s` Values `%(value)s` which is greater than `%(limit)s`.',
}


class CommonException(Exception):

    def __init__(self, enum_cls):
        self.code = enum_cls.code
        self.msg = enum_cls.msg
        self.enum_cls = enum_cls #状态码枚举类
        super().__init__()


class BusinessException(CommonException):
    """业务异常类"""
    pass

class APIException(Exception):
    message = 'An unknown exception occurred.'
    code = 'InternalError'
    icode = -1

    def __init__(self, **kwargs):  # 如果入参是一个列表，需要格式化，而不能依赖python的repr，否则，会暴露后端语言。
        self.kwargs = kwargs
        # 如果报错时提供了错误信息，则直接使用，否则使用预定义格式的错误信息
        if 'msg' in kwargs:
            self.message = kwargs['msg']
        else:
            _msg = EXCEPTION_MESSAGE_MAP[kwargs['message'] if 'message' in kwargs else self.__class__.code]
            try:
                self.message = _msg % self.kwargs
            except:
                context.Language = 'en-US'
                _msg = EXCEPTION_MESSAGE_MAP[kwargs['message'] if 'message' in kwargs else self.__class__.code]
                self.message = _msg % self.kwargs


        if 'icode' in kwargs:
            self.icode = kwargs['icode']

    def __str__(self):
        return self.message

    def validate_message(self, message):
        assert message in EXCEPTION_MESSAGE_MAP.values(
        ), "%s not in EXCEPTION_MESSAGE_MAP" % message
        return message

class UnknownAPIRequest(APIException):
    """
    The request is not recognized.
    """
    code = 'UnknownAPIRequest'

class InternServerException(APIException):  # TODO(skipzhang) 这里需要整体改名..目前还没做
    code = 'InternalError'


class UnknownParameter(APIException):
    code = 'UnknownParameter'


class InvalidRegionNotFound(APIException):
    code = 'InvalidRegion.NotFound'


class MissingAction(APIException):
    """
    The request is missing an action.
    """
    code = 'MissingAction'


class InvalidInput(APIException):
    code = 'InvalidInput'


class InvalidInput_JSON(InvalidInput):
    code = 'InvalidInput.JSON'


class InvalidZone(APIException):
    """
    The specified Zone ID is unavailable.
    """
    code = 'InvalidZone'


class ResourceNotFound(APIException):
    code = 'ResourceNotFound'


class InvalidParameter(APIException):
    """
    A parameter specified in a request is not valid,
    is unsupported, or cannot be used. The returned
    message provides an explanation of the error value.
    For example, if you are launching an instance, you
    can't specify a security group and subnet that are in
    different VPCs.
    """
    code = 'InvalidParameter'

    class FormatError(APIException):
        code = 'InvalidParameter.FormatError'

    class LBIdNotFound(APIException):
        code = 'InvalidParameter.LBIdNotFound'

    class ListenerIdNotFound(APIException):
        code = 'InvalidParameter.ListenerIdNotFound'

    class ProtocolCheckFailed(APIException):
        code = 'InvalidParameter.ProtocolCheckFailed'

    class PortCheckFailed(APIException):
        code = 'InvalidParameter.PortCheckFailed'

    class LocationNotFound(APIException):
        code = "InvalidParameter.LocationNotFound"

    class SomeRewriteNotFound(APIException):
        code = "InvalidParameter.SomeRewriteNotFound"

    class RewriteAlreadyExist(APIException):
        code = "InvalidParameter.RewriteAlreadyExist"

    class RegionNotFound(APIException):
        code = "InvalidParameter.RegionNotFound"

    class ClientTokenLimitExceeded(APIException):
        code = "InvalidParameter.ClientTokenLimitExceeded"


class InvalidParameterCombination(APIException):
    """
    Indicates an incorrect combination of parameters, or
    a missing parameter. For example, trying to terminate
    an instance without specifying the instance ID.
    """
    code = 'InvalidParameterCombination'

    class ZoneSoldOutForSpecifiedInstance(APIException):
        """The specified instance type `%(instance_type)s` is sold out in zone `%(zone)s`."""
        code = 'InvalidParameterCombination.ZoneSoldOutForSpecifiedInstance'


class InvalidParameterValue(APIException):
    """
    A value specified in a parameter is not valid, is
    unsupported, or cannot be used. Ensure that you
    specify a resource by using its full ID. The returned
    message provides an explanation of the error value.
    """
    code = 'InvalidParameterValue'

    class Range(APIException):
        """
        A value specified in a parameter is not valid, is
        unsupported, or cannot be used. Ensure that you
        specify a resource by using its full ID. The returned
        message provides an explanation of the error value.
        """
        code = 'InvalidParameterValue.Range'

    class Length(APIException):
        code = 'InvalidParameterValue.Length'

    class Duplicate(APIException):
        code = 'InvalidParameterValue.Duplicate'

    class NotInTheSameProject(APIException):
        code = 'InvalidParameterValue.NotInTheSameProject'

    class InvalidFilter(APIException):
        """
        The specified filter is not valid.
        """
        code = 'InvalidParameterValue.InvalidFilter'


class MissingParameter(APIException):
    """
    The request is missing a required parameter. Ensure
    that you have supplied all the required parameters for
    the request; for example, the resource ID.
    """
    code = 'MissingParameter'


class InvalidParameterValueLimitExceeded(APIException):
    """
    The request parameter uses too many values.
    """
    code = 'InvalidParameterValue.LimitExceeded'


class InternalError(APIException):
    """
    An internal error has occurred. Retry your request,
    but if the problem persists, contact us with details by
    posting a message.
    """
    code = 'InternalError'


class UnauthorizedOperation(APIException):
    """
    UnauthorizedOperation.
    """
    code = 'UnauthorizedOperation'


class AuthFailure(APIException):
    """
    AuthFailure
    """
    code = 'AuthFailure'

    class TokenFailure(APIException):
        code = 'AuthFailure.TokenFailure'


class ResourceInsufficient(APIException):
    """
    ResourceInsufficient.
    """
    code = 'ResourceInsufficient'


class LimitExceeded(APIException):
    """
    LimitExceeded.
    """
    code = 'LimitExceeded'


class FailedOperation(APIException):
    """
    FailedOperation.
    """
    code = 'FailedOperation'

    class InvalidLBStatus(APIException):
        code = "FailedOperation.InvalidLBStatus"

    class InvalidAccountStatus(APIException):
        code = "FailedOperation.InvalidAccountStatus"

    class InvalidCLBStatus(APIException):
        code = "FailedOperation.InvalidCLBStatus"

    class InvalidNetWorkStatus(APIException):
        code = "FailedOperation.InvalidNetWorkStatus"

    class InvalidHealthCheckStatus(APIException):
        code = "FailedOperation.InvalidHealthCheckStatus"

    class ResourceInOperating(APIException):
        code = "FailedOperation.ResourceInOperating"


class MutexOperationTaskRunning(APIException):
    code = "MutexOperation.TaskRunning"


class InvalidLocationId(APIException):
    """
    InvalidLocationId
    """
    code = "InvalidLocationId"

    class NotFound(APIException):
        """
        LocationId not found
        """
        code = "InvalidLocationId.NotFound"


class NotFindLoadBalancer(APIException):
    code = "NotFindLoadBalancer"


class CreateGaFail(APIException):
    code = "CreateGaFail"

