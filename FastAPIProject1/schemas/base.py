from datetime import datetime
from pydantic import BaseModel, Field
from pydantic import BaseModel, ConfigDict
from typing import Optional

from sqlalchemy import alias


class NewsItemBase(BaseModel):
    id:int
    title:str
    description:Optional[str]=None
    image:Optional[ str]=None
    author:Optional[str]=None
    category:int=Field(alias="categoryId")
    view:int
    publish_time:Optional[datetime]=Field(None,alias="publishedTime")
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True)


