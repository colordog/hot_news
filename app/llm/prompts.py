from typing import Dict, List, Optional

from app.llm.schemas import ChatMessage, HotNewsItem


PROMPT_VERSION = "v1"

HOT_SUMMARY_SYSTEM_PROMPT = """你是一名资深中文热点编辑，负责把全网热点整理成简洁、准确、有信息密度的日报。

你的目标：
1. 基于当前新闻，提炼今天最重要的话题和趋势。
2. 结合上一版总结，指出延续、变化、升温和降温的话题。
3. 输出内容必须忠于输入，不编造事实，不补充输入中没有的信息。
4. 语言简洁、自然、适合直接展示给客户端用户阅读。

输出要求：
1. 使用 Markdown 输出。
2. 必须包含以下四个小节：
   - 今日总览
   - 核心话题
   - 与上一版相比
   - 后续关注
3. “核心话题”请使用 3 到 6 条编号列表。
4. 如果没有上一版总结，明确写“暂无上一版总结可对比”。
5. 如果输入新闻信息不足，不要猜测，用“信息有限”说明。"""


def build_hot_summary_messages(
    date_str: str,
    previous_summary: Optional[Dict],
    news_items: List[HotNewsItem],
) -> List[Dict[str, str]]:
    previous_summary_text = "暂无上一版总结可对比。"
    if previous_summary and previous_summary.get("summary"):
        previous_summary_text = previous_summary["summary"]

    news_lines = []
    for index, item in enumerate(news_items, start=1):
        extras = []
        if item.rank not in (None, ""):
            extras.append(f"排名: {item.rank}")
        if item.score not in (None, ""):
            extras.append(f"热度: {item.score}")
        extra_text = f" | {' | '.join(extras)}" if extras else ""
        content = item.content.strip() if item.content else ""
        if len(content) > 120:
            content = f"{content[:120]}..."
        news_lines.append(
            f"{index}. [{item.platform}] {item.title}{extra_text}\n"
            f"链接: {item.url or '无'}\n"
            f"补充: {content or '无'}"
        )

    user_prompt = f"""请基于以下信息生成 {date_str} 的当前热点总结。

上一版总结：
{previous_summary_text}

当前热点新闻：
{chr(10).join(news_lines) if news_lines else '暂无新闻数据'}
"""

    messages = [
        ChatMessage(role="system", content=HOT_SUMMARY_SYSTEM_PROMPT).dict(),
        ChatMessage(role="user", content=user_prompt).dict(),
    ]
    return messages
