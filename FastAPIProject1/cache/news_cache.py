from typing import Any, Dict

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY="news:categories"
#获取新闻分类缓存
async def get_cached_categories():
   return await get_json_cache(CATEGORIES_KEY)
#写入新闻分类缓存
async def set_cached_categories(data:list[Dict[str,Any]],expire:int=7200):
   return await set_cache(CATEGORIES_KEY,data,expire)





