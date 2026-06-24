from datetime import datetime
from typing import Optional

import pytz
from fastapi import APIRouter

from app.llm import HotSummaryService
from app.utils.logger import log


router = APIRouter()
SHANGHAI_TZ = pytz.timezone("Asia/Shanghai")


@router.get("/hot-summary")
async def get_hot_summary(date: Optional[str] = None, refresh: bool = False):
    """
    获取 LLM 生成的热点总结

    - **date**: 可选，指定日期，格式为 YYYY-MM-DD，默认为当天
    - **refresh**: 可选，是否强制重新生成，默认为 False
    """
    try:
        if not date:
            date = datetime.now(SHANGHAI_TZ).strftime("%Y-%m-%d")

        service = HotSummaryService()
        return service.get_summary(date, refresh)
    except Exception as exc:
        log.error(f"Error in LLM hot summary API: {exc}")
        return {
            "status": "error",
            "message": str(exc),
            "date": date or datetime.now(SHANGHAI_TZ).strftime("%Y-%m-%d"),
        }


@router.get("/hot-summary/latest")
async def get_latest_hot_summary():
    """
    获取最新一版 LLM 热点总结
    """
    try:
        service = HotSummaryService()
        return service.get_latest_summary()
    except Exception as exc:
        log.error(f"Error in latest LLM hot summary API: {exc}")
        return {
            "status": "error",
            "message": str(exc),
            "date": datetime.now(SHANGHAI_TZ).strftime("%Y-%m-%d"),
        }
