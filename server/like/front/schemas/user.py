from datetime import datetime
import re
from typing import Union

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Literal

class UserCenterOut(BaseModel):
    """个人中心返回"""
    id: int  # 主键
    sn: int  # 编号
    avatar: str  # 头像
    realName: str = Field(alias='real_name')  # 真实姓名
    nickname: str  # 用户昵称
    username: str  # 用户账号
    mobile: str  # 用户电话

    class Config:
        from_attributes = True


class UserInfoOut(UserCenterOut):
    """个人信息返回"""
    sex: int  # 用户性别
    isPassword: Union[bool, None] = Field(alias='is_password', default=False)  # 用户性别
    isBindMnp: Union[bool, None] = Field(alias='is_bind_mnp', default=False)  # 用户性别
    version: Union[str, None] = Field(alias='is_bind_mnp', default=None) # 版本
    createTime: datetime = Field(alias='create_time')  # 创建时间

    class Config:
        from_attributes = True


class UserEditIn(BaseModel):
    """编辑信息参数"""
    field: str  # 字段
    value: str  # 值


class UserChangePwdIn(BaseModel):
    """修改密码参数"""
    password: str = Field(min_length=6, max_length=20)  # 密码,必须是6-20位字母+数字组合
    old_password: str = Field(alias='oldPassword')  # 当前密码

    @field_validator('password')
    def validate_password(cls, v):
        # 使用Python标准re库，支持look-around断言
        pattern = r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$'
        if not re.match(pattern, v):
            raise ValueError('密码必须是6-20位字母和数字的组合（不能全是字母或全是数字）')
        return v


class UserBindMobileIn(BaseModel):
    """绑定手机参数"""
    type: Literal['bind', 'change']
    mobile: str = Field(pattern='^[1][3,4,5,6,7,8,9][0-9]{9}$')  # 手机号
    code: str  # 验证码


class UserMnpMobileIn(BaseModel):
    """微信手机号参数"""
    code: str  # 验证码
