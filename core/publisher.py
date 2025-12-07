import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.utils import logger, get_env
import requests

GMAIL_USER = get_env("GMAIL_USER")
GMAIL_APP_PASSWORD = get_env("GMAIL_APP_PASSWORD")
BLOGGER_EMAIL = get_env("BLOGGER_EMAIL")  # Blogger's post-by-email address; check Blogger setting

def publish_blogger_via_email(subject: str, html_body: str, category: str = "未分類"):
    """
    Publish to Blogger using 'Post by email' feature.
    """
    if not GMAIL_USER or not GMAIL_APP_PASSWORD or not BLOGGER_EMAIL:
        logger.error("Gmail or Blogger email not configured.")
        return False
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = BLOGGER_EMAIL
        msg['Subject'] = f"{subject} #{category}"
        msg.attach(MIMEText(html_body, 'html'))

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        logger.info("Published to Blogger via email.")
        return True
    except Exception as e:
        logger.exception("Failed to publish to Blogger: %s", e)
        return False

def publish_telegram(bot_token: str, channel_id: str, text: str):
    """
    Publish plain text / html to Telegram channel (bot must be admin of channel).
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": channel_id, "text": text, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload, timeout=10)
        r.raise_for_status()
        logger.info("Published to Telegram.")
        return True
    except Exception as e:
        logger.exception("Failed to publish to Telegram: %s", e)
        return False

def publish_allPlatforms(title: str, html_body: str, category: str = "未分類", telegram=None):
    """
    Basic wrapper: currently Blogger + Telegram
    """
    ok1 = publish_blogger_via_email(title, html_body, category)
    ok2 = True
    if telegram:
        ok2 = publish_telegram(telegram.get("token"), telegram.get("channel"))
    return ok1 and ok2
