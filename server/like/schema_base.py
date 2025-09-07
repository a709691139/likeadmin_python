from datetime import datetime
from typing import Union, TypeVar, Generic, Sequence

from fastapi import Query
from fastapi_pagination.bases import AbstractParams, AbstractPage, RawParams
from pydantic import BaseModel
from pydantic_core.core_schema import ValidationInfo

T = TypeVar("T")
C = TypeVar("C")


class PageParams(BaseModel, AbstractParams):
    pageNo: int = Query(1, ge=1, description='Page Number')
    pageSize: int = Query(20, gt=0, le=60, description='Page Size')

    def to_raw_params(self) -> RawParams:
        offset = (self.pageNo - 1) * self.pageSize
        return RawParams(limit=self.pageSize, offset=offset)


class PageInationResult(AbstractPage[T], Generic[T]):
    """
    分页结果封装
        items: 返回集列表
        total: 结果总数
    """
    count: int
    pageNo: int
    pageSize: int
    lists: Sequence[T]

    __params_type__ = PageParams

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: PageParams):
        return cls(lists=items, count=total, pageNo=params.pageNo, pageSize=params.pageSize)


def empty_to_none(v: str, info: ValidationInfo | None = None) -> Union[str, None]:
    """替换空字符为None"""
    if v == '':
        return None
    return v

# 新增 info 可选参数，兼容 Pydantic 传递的验证上下文
def validate_str(v, info: ValidationInfo | None = None):
    if v is None:
        return None
    if not isinstance(v, str):
        v = str(v)  # 非字符串类型转为字符串
    return v

class EmptyStrToNone(str):
    """空字符串替换类型：将空字符串转为 None，非字符串类型会先转为字符串"""

    @classmethod
    def __get_validators__(cls):
        # 按顺序返回验证器
        yield validate_str
        yield empty_to_none
    