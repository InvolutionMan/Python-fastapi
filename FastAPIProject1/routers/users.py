from fastapi import APIRouter, Query, FastAPI, dependencies, HTTPException
from fastapi.params import Depends
from starlette import status

from models.users import User
from utils.auth import get_current_user
from config.db_conf import get_db
from crud import users
from crud import news
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserInfoBase, \
    UserUpdateRequest, UserChangePasswordRequest
from utils.response import success_response

router=APIRouter(prefix="/api/user",tags=["user"])

@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
    existing_user=await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=400,detail="用户已存在")

    user=await users.create_user(db,user_data)
    token=await users.create_token(db,user.id)
    # return {
    #         "code":200,
    #         "message":"注册成功",
    #         "data": {
    #             "token":token,
    #             "userInfo":{
    #                 "id":user.id,
    #                 "username":user.username,
    #                 "bio":user.bio,
    #                 "avatar":user.avatar
    #             }
    #         }
    # }
    response_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功",data=response_data)

@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession=Depends(get_db)):
   user=await users.authenticate_user(db,user_data.username,user_data.password)
   if not user:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
   token=await users.create_token(db,user.id)
   resource_data=UserAuthResponse(token=token,user_info=UserInfoResponse.model_validate(user))
   return success_response(message="登录成功",data=resource_data)


@router.get("/info")
async def get_user_info(user:User=Depends(get_current_user)):
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))

@router.put("/update")
async def update_user_info(user_data:UserUpdateRequest,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
    result=await users.update_user(db,user_data,user.username)
    return success_response(message="更新成功",data=UserInfoResponse.model_validate(result))

@router.put("/password")
async def update_password(
        password_data:UserChangePasswordRequest,
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    result=await users.change_password(
        db,
        user,
        password_data.old_password,
        password_data.new_password
    )
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="修改密码失败")
    return success_response(message="修改密码成功")





