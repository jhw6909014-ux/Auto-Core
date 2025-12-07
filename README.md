# Auto-Core

Core library for AutoBots (RSS -> AI -> Publish).  
Contains modules for RSS fetch, AI generation, image caching, affiliate links, DB.

## Quick start

1. Set env variables (GOOGLE_API_KEY, GMAIL_USER, GMAIL_APP_PASSWORD, BLOGGER_EMAIL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID)
2. pip install -e .
3. python -c "from core.db import init_db; init_db()"
