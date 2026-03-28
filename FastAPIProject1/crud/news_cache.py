from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, values
from sqlalchemy.orm.sync import update
from sqlalchemy import update

from models.news import Category, News
from cache.news_cache import get_cached_categories, set_cached_categories


async def get_categories(db:AsyncSession,skip:int=0,limit:int=100):
    #从缓冲中获取
    cached_categories=await get_cached_categories()
    if cached_categories:
        return cached_categories



    stmt=select(Category).offset(skip).limit(limit)
    result=await db.execute(stmt)
    categories= result.scalars().all()

#写入缓存
    if categories:
        categories=jsonable_encoder(categories)
        await set_cached_categories(categories)
#返回数据
    return categories




async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    stmt=select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result=await db.execute(stmt)
    return result.scalars().all()

async def get_news_count(db:AsyncSession,category_id:int):
    stmt=select(func.count(News.id)).where(News.category_id==category_id)
    result=await db.execute(stmt)
    return result.scalar_one()

async def get_news_detail(db:AsyncSession,news_id:int):
    stmt=select(News).where(News.id==news_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_views(db:AsyncSession,news_id:int):
    stmt=update(News).where(News.id==news_id).values(views=News.views+1)
    result=await db.execute(stmt)
    await db.commit()
    return result.rowcount>0

async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit:int=5):
    stmt=select(News).where(News.category_id==category_id,News.id!=news_id).order_by(News.views.desc(),News.publish_time.desc()).limit(limit)
    result=await db.execute(stmt)
    related_news= result.scalars().all()
    #列表推导式
    return [{"id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "view":news_detail.views
        }for news_detail in related_news]