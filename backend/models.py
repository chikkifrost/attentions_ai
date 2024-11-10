from pydantic import BaseModel
from datetime import datetime
from typing import List

class ResearchPaper(BaseModel):
    id: str
    title: str
    authors: List[str]
    abstract: str
    published: datetime
    url: str