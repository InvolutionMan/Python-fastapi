#数据类型校验
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class UserRequest(BaseModel):
    username:str
    password:str

class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, description="昵称", max_length=50)
    avatar: Optional[str] = Field(None, description="头像URL", max_length=255)
    gender: Optional[str] = Field(None, description="性别", max_length=10)
    bio: Optional[str] = Field(None, description="个人简介", max_length=500)


class UserInfoResponse(UserInfoBase):
     id: int
     username:str
     model_config = ConfigDict(
         from_attributes=True,
     )

class UserAuthResponse(BaseModel):
    token:str
    user_info:UserInfoResponse=Field(...,alias="userInfo")
    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

class UserUpdateRequest(UserInfoBase):
    nickname: str=None
    avatar: str= None
    gender : str= None
    bio :str= None
    phone:str= None

class UserChangePasswordRequest(BaseModel):
    old_password:str=Field(...,alias="oldPassword",description="旧密码")
    new_password:str=Field(...,alias="newPassword",description="新密码")




