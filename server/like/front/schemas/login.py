from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field, field_validator
import re

from like.common.enums import LoginTypeEnum, LoginClientEnum


class FrontLoginCheckOut(BaseModel):
    """
    登录管理 返回信息
    """
    id: int
    token: str
    isBindMobile: bool
    class Config:
        from_attributes = True


class FrontRegisterIn(BaseModel):
    """
    注册 入参
    """
    username: str = Field(min_length=3, max_length=12, description="用户名必须包含字母和数字，3-12位")
    password: str = Field(min_length=6, max_length=12)
    client: LoginClientEnum

    @field_validator('username')
    def validate_username(cls, v):
        # 检查是否只包含字母和数字
        if not re.match(r'^[0-9A-Za-z]+$', v):
            raise ValueError('用户名只能包含字母和数字')
        
        # 检查是否包含至少一个数字
        if not re.search(r'[0-9]', v):
            raise ValueError('用户名必须包含至少一个数字')
        
        # 检查是否包含至少一个字母
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('用户名必须包含至少一个字母')
        
        return v


class FrontLoginCheckIn(BaseModel):
    """
    手机端-登录管理 入参
    """
    scene: LoginTypeEnum # 登录方式
    client: LoginClientEnum  # 登录端
    username: str = Field(default=None)
    mobile: str = Field(default=None)
    password: str = Field(default=None)
    code: str = Field(default=None)
