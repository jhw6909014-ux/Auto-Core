import os
import hashlib
import logging
from slugify import slugify
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("auto_core")

def make_slug(text: str) -> str:
    return slugify(text)[:120]

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def get_env(key: str, default=None):
    return os.environ.get(key, default)
