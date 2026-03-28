from fastapi import APIRouter, Query, FastAPI, dependencies, HTTPException
from fastapi.params import Depends
from config.db_conf import get_db
from crud import news_cache
from crud import news
from sqlalchemy.ext.asyncio import AsyncSession
router=APIRouter(prefix="/api/news",tags=["news"])



@router.get("/categories")
async def get_categories(skip:int=0,limit:int=100,db:AsyncSession=Depends(get_db)):
    categories=await news_cache.get_categories(db,skip,limit)
    return {"code":200,
            "message":"获取新闻分类成功",
            "data": categories
            }

@router.get("/list")
async def get_news_list(
        db:AsyncSession=Depends(get_db),
        category_id:int=Query(...,alias="categoryId"),
        page:int=1,
        page_size:int=Query(10,le=100,alias="pageSize"),
):
    offset=(page-1)*page_size
    news_list=await news.get_news_list(db,category_id,offset,page_size)
    total=await news.get_news_count(db,category_id)
    has_More=(offset+len(news_list))<total
    return {
        "code":200,
        "message":"success",
        "data": {
            "list":news_list,
            "total":total,
            "hasMore":has_More
        }
    }

@router.get("/detail")
async def get_news_detail(news_id:int=Query(...,alias="id"),db:AsyncSession=Depends(get_db)):
    news_detail=await news.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")

    views_res=await news.increase_news_views(db,news_id)
    if not views_res:
        raise HTTPException(status_code=404,detail="更新新闻浏览量失败")

    relate_news=await news.get_related_news(db,news_detail.id,news_detail.category_id)


    return {
        "code":200,
        "message":"success",
        "data":{
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "view":news_detail.views,
            "relatedNews":relate_news
        }
    }












