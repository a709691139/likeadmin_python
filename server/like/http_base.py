import inspect
from collections import namedtuple
from datetime import datetime
from functools import wraps
from typing import Callable, TypeVar

from pydantic import BaseModel
import pytz
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from databases.core import Record

from .config import get_settings

__all__ = ['HttpCode', 'HttpResp', 'unified_resp']

RT = TypeVar('RT')  # 返回类型
HttpCode = namedtuple('HttpResp', ['code', 'msg'])


class HttpResp:
    """HTTP响应结果
    """
    SUCCESS = HttpCode(200, '成功')
    FAILED = HttpCode(300, '失败')
    PARAMS_VALID_ERROR = HttpCode(310, '参数校验错误')
    PARAMS_TYPE_ERROR = HttpCode(311, '参数类型错误')
    REQUEST_METHOD_ERROR = HttpCode(312, '请求方法错误')
    ASSERT_ARGUMENT_ERROR = HttpCode(313, '断言参数错误')

    LOGIN_ACCOUNT_ERROR = HttpCode(330, '登录账号或密码错误')
    LOGIN_DISABLE_ERROR = HttpCode(331, '登录账号已被禁用了')
    TOKEN_EMPTY = HttpCode(332, 'token参数为空')
    TOKEN_INVALID = HttpCode(333, 'token参数无效')

    NO_PERMISSION = HttpCode(403, '无相关权限')
    REQUEST_404_ERROR = HttpCode(404, '请求接口不存在')

    SYSTEM_ERROR = HttpCode(500, '系统错误')
    SYSTEM_TIMEOUT_ERROR = HttpCode(504, '请求超时')


def unified_resp(func: Callable[..., RT]) -> Callable[..., RT]:
    """统一响应格式
        接口正常返回时,统一响应结果格式
    """

    @wraps(func)
    async def wrapper(*args: any, **kwargs: any) -> RT:
        # 执行原函数获取响应
        if inspect.iscoroutinefunction(func):
            resp = await func(*args, **kwargs) or []
        else:
            resp = func(*args, **kwargs) or []
        
        resp_dict = jsonable_encoder(resp, by_alias=False)

        # 确认配置
        settings = get_settings()
        target_tz = pytz.timezone(settings.timezone)
        fmt = settings.datetime_fmt

        # 递归处理所有 datetime和Record
        def deep_convert_value(obj):
            if isinstance(obj, datetime):
                # 确保时区正确转换
                if obj.tzinfo:
                    localized = obj.astimezone(target_tz)
                else:
                    localized = pytz.utc.localize(obj).astimezone(target_tz)
                return localized.strftime(fmt)
            elif isinstance(obj, dict):
                return {k: deep_convert_value(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [deep_convert_value(item) for item in obj]
            return obj
        
        # 对转换后的字典进行二次处理（确保所有 datetime 被格式化）
        processed_data = deep_convert_value(resp_dict)
        # 构建响应
        return JSONResponse(
            content={
                'code': HttpResp.SUCCESS.code,
                'msg': HttpResp.SUCCESS.msg,
                'data': processed_data
            },
            media_type='application/json;charset=utf-8'
        )
    
    return wrapper
