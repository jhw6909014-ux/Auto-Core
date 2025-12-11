import os
import time
import logging
import urllib.parse
import google.generativeai as genai
from typing import Dict, Optional

# --- 設定 Log (確保出錯時你看得到) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- 【關鍵設定】你的蝦皮分潤 ID ---
# 這裡直接寫入你的 ID，程式會自動讀取
SHOPEE_AFFILIATE_ID = "16332290023"

# --- 設定 Google API ---
# 優先從 Secrets 讀取，讀不到則報錯
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    logger.error("❌ 嚴重錯誤：未偵測到 GOOGLE_API_KEY，請去 GitHub Secrets 設定！")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# --- 功能 1: 蝦皮分潤按鈕產生器 (含 ID) ---
def create_shopee_button(keyword: str) -> str:
    """
    根據關鍵字生成帶有你分潤 ID 的蝦皮搜尋按鈕
    """
    # 1. 處理關鍵字 (URL 編碼，避免中文亂碼)
    safe_keyword = urllib.parse.quote(keyword)
    
    # 2. 組合網址
    # 注意：雖然這不能保證 100% 追蹤 (蝦皮通常要求用轉換後的連結)，
    # 但我們將 ID 放入 utm 參數，這是自動化能做的最大努力。
    base_url = "https://shopee.tw/search"
    params = f"?keyword={safe_keyword}&utm_source=affiliate&utm_medium=seller&utm_campaign={SHOPEE_AFFILIATE_ID}"
    shopee_url = base_url + params
    
    # 3. 生成 2026 風格的高點擊按鈕 HTML (橘色系 + 陰影)
    button_html = f"""
    <div style="margin: 40px 0; text-align: center; padding: 20px; background-color: #fdfdfd; border-radius: 8px; border: 1px dashed #ee4d2d;">
        <p style="font-size: 16px; color: #555; margin-bottom: 15px; font-weight: bold;">
            💡 讀者專屬優惠查詢
        </p>
        <a href="{shopee_url}" target="_blank" rel="nofollow noopener" 
           style="background-color: #ee4d2d; color: white; padding: 14px 28px; 
                  text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 18px; 
                  box-shadow: 0 4px 6px rgba(238, 77, 45, 0.3); transition: all 0.3s ease;">
           🔍 前往蝦皮搜尋「{keyword}」最新價格
        </a>
        <p style="font-size: 12px; color: #999; margin-top: 10px;">
            (點擊按鈕將開啟蝦皮購物搜尋頁面)
        </p>
    </div>
    """
    return button_html

# --- 功能 2: 2026 未來趨勢提示詞 (Prompt) ---
def generate_prompt(title: str, summary: str, style: str) -> str:
    """
    生成高轉化率的 Prompt，強制要求 AI 產出表格
    """
    persona = style if style else "專業部落客"
    
    return f"""
    你是一位【{persona}】。請根據以下新聞，寫一篇繁體中文的部落格文章。
    
    【新聞標題】: {title}
    【新聞摘要】: {summary}
    
    【寫作指令 - 目標是高流量與高互動】:
    1. **標題**: 請自訂一個吸引人的標題 (Clickbait)，要讓人想點擊。
    2. **HTML 格式**: 請直接輸出 HTML 代碼 (不要用 Markdown ```html 包裹)。
       - 使用 <h2> 作為段落標題。
       - 使用 <p> 作為內文。
    3. **內容結構**:
       - **開頭**: 用口語化方式快速帶出新聞重點。
       - **分析**: 這則新聞對讀者有什麼具體影響？
       - **核心比較 (最重要)**: 請製作一個 HTML 表格 (<table>)，列出與此新聞相關的 3 個產品或解決方案的比較 (包含：名稱、優點、推薦指數)。
    4. **結尾導購**: 引導讀者去尋找相關工具或產品。
    5. **語氣**: {persona} 的口吻，親切且專業。
    
    請確保內容豐富，字數約 600-800 字。
    """

# --- 功能 3: 文章生成主程式 (含防呆機制) ---
def generate_article(title: str, summary: str, lang: str = "zh-TW", style: str = "專業部落客") -> Dict:
    """
    呼叫 AI 生成文章，並自動插入你的蝦皮分潤按鈕
    """
    # 1. 檢查 API Key 是否存在
    if not GOOGLE_API_KEY:
        logger.error("❌ 生成終止：沒有 API Key")
        return {}

    # 2. 準備提示詞
    prompt = generate_prompt(title, summary, style)
    
    # 3. 呼叫 AI (重試機制: 最多試 3 次)
    max_retries = 3
    generated_text = ""
    
    logger.info(f"🤖 AI 開始撰寫: {title} (風格: {style})")
    
    for attempt in range(max_retries):
        try:
            # 使用 Gemini 1.5 Flash (速度快、免費、適合大量文字)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            
            if response.text:
                generated_text = response.text
                # 如果 AI 雞婆加了 Markdown 標記，把它清掉
                generated_text = generated_text.replace("```html", "").replace("```", "")
                break # 成功就跳出
        except Exception as e:
            logger.warning(f"⚠️ AI 連線失敗 (第 {attempt+1} 次): {e}")
            time.sleep(2) # 休息 2 秒再試

    # 4. 檢查結果
    if not generated_text:
        logger.error("❌ AI 最終生成失敗，跳過此篇")
        return {}

    # 5. 【關鍵】植入你的蝦皮按鈕
    # 策略：取標題的前幾個關鍵字來搜尋，這樣最準
    # 這裡我們簡單取標題前 10 個字，或是你可以讓 AI 另外生成關鍵字
    search_keyword = title[:15].replace("【", "").replace("】", "") 
    shopee_btn = create_shopee_button(search_keyword)
    
    # 將按鈕加在文章最後面 (這是一定會被看到的黃金位置)
    final_html = f"{generated_text}\n{shopee_btn}"

    logger.info(f"✅ 文章生成與按鈕植入成功！")

    return {
        "title": title, 
        "html_body": final_html,
        "category": "Uncategorized" # Run.py 會再覆蓋這個
    }

# --- 測試區 (讓你本地跑的時候可以測試) ---
if __name__ == "__main__":
    # 本地測試用 (不會在 GitHub Actions 裡執行)
    print("測試生成按鈕：")
    print(create_shopee_button("測試商品"))
