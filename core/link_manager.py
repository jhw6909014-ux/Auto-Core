from typing import Optional

# 範例聯盟庫（你可以把更多連結放到外部 JSON 或 DB）
AFFILIATES = {
    "food": [
        {"name": "shopee", "url": "https://s.shopee.tw/2VkTZLnxpK"},
        {"name": "momo", "url": "https://www.momoshop.com.tw/food_link_example"},
        {"name": "amazon", "url": "https://www.amazon.com/s?k=food"}
    ],
    "tech": [
        {"name": "amazon", "url": "https://www.amazon.com/s?k=tech"},
        {"name": "shopee", "url": "https://s.shopee.tw/tech_link_example"}
    ],
    "default": [
        {"name": "shopee", "url": "https://s.shopee.tw/2VkTZLnxpK"}
    ]
}

def choose_affiliate_link(title: str, category_hint: str = "") -> str:
    key = category_hint if category_hint in AFFILIATES else "default"
    arr = AFFILIATES.get(key, AFFILIATES["default"])
    # 目前採取最簡單選擇：回傳第一個
    if arr:
        return arr[0]["url"]
    return ""
