import os
import time
import json
from core.utils import logger, hash_text
from typing import Dict

# 注意：此處示範一個泛用介面，實際與你使用的 SDK (google.generativeai) 要做對應調整。
# 先使用環境變數 GOOGLE_API_KEY
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def generate_prompt(title: str, summary: str, lang: str = "zh-TW", style: str = "zh_style_1") -> str:
    # 模板很簡單：可在 templates 資料夾放更複雜的 prompt
    return f"請把以下資訊改寫成繁體中文（若lang != zh-TW請翻譯）：\n標題: {title}\n摘要: {summary}\n\n請用吸引人的食物部落客語氣寫三段，分段清楚，並在結尾放置購買按鈕區塊的 HTML。"

def generate_article(title: str, summary: str, lang: str = "zh-TW", style: str = "zh_style_1") -> Dict:
    """
    回傳 dict: { 'title': ..., 'html_body': ..., 'category': ... }
    這裡示範成同步呼叫外部 model（請根據你的 SDK 替換）
    """
    prompt = generate_prompt(title, summary, lang, style)
    # ---- 這裡需要根據你實際使用的 model 呼叫方式改寫 ----
    # 範例：直接把 summary 包裝成 html，實際上要呼叫 Google / OpenAI
    html_body = f"<h2>{title}</h2><p>{summary}</p><p>（AI 產文示範，請換成實際 model 呼叫）</p>"
    category = "未分類"
    return {"title": title, "html_body": html_body, "category": category}
