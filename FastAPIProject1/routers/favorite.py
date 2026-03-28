from itertools import count

from fastapi import Query
from fastapi import APIRouter, Depends
from sqlalchemy import alias
from sqlmodel.ext.asyncio.session import AsyncSession

from config.db_conf import get_db
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse

router=APIRouter(prefix="/api/favorite",tags=["favorite"])

@router.get("/check")
async def  check_favorite(
        new_id:int=Query(...,alias="newsId"),
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    is_favorited=await favorite.is_news_favorite(db,user.id,new_id)
    return success_response(message="获取收藏状态成功",data=FavoriteCheckResponse(isFavorite=is_favorited))

@router.post("/add")
async def add_favorite(
        data:FavoriteAddRequest,
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    result=await favorite.add_favorite(db,user.id,data.news_id)
    return success_response(message="收藏成功",data=result)

@router.delete("/remove")
async def remove_favorite(
        new_id:int=Query(...,alias="newsId"),
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    result=await favorite.remove_favorite(db,user.id,new_id)
    if not result:
        from fastapi import HTTPException
        from starlette import status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="收藏记录不存在")
    return success_response(message="取消收藏成功")

@router.get("/list")
async def get_favorite_list(
        page:int=Query(1,ge=1),
        page_size:int=Query(10,ge=1,le=100,alias="pageSize"),
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    rows,total=await favorite.get_favorite_list(db,user.id,page,page_size)
    favorite_list=[{
        **news.__dict__,
        "favorite_time":favorite_time,
        "favorite_id":favorite_id,
    } for news,favorite_time,favorite_id in rows]#orm需转换成字典形式
    has_more=total>page*page_size
    data=FavoriteListResponse(list=favorite_list,total=total,hasMore=has_more)#构建类型
    return success_response(message="获取收藏列表成功",data=data)

@router.delete("/clear")
async def clear_favorite(
        user:User=Depends(get_current_user),
        db:AsyncSession=Depends(get_db)
):
    result=await favorite.remove_all_favorites(db,user.id)
    return success_response(message=f"清空了{result}条数据",)
















