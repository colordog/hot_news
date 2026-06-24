from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str
    content: str


class HotNewsItem(BaseModel):
    platform: str
    title: str
    url: str = ""
    content: str = ""
    score: Optional[Any] = None
    rank: Optional[Any] = None


class HotSummaryResult(BaseModel):
    status: str
    message: str
    date: str
    summary: str = ""
    previous_summary_date: Optional[str] = None
    news_count: int = 0
    platforms: List[str] = Field(default_factory=list)
    model: str = ""
    generated_at: str = ""
    prompt_version: str = "v1"
    metadata: Dict[str, Any] = Field(default_factory=dict)
