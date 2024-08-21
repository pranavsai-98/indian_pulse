from pydantic import BaseModel
from typing import List, Dict, Optional


class Article(BaseModel):
    headline: str
    published_date: str
    main_content: str
    main_image_url: str
    url: str
    summary: str
    news_rating: int
    category: str


class StateNews(BaseModel):
    state: str
    articles: List[Article]


class AllStateNews(BaseModel):
    __root__: Dict[str, List[Article]]
