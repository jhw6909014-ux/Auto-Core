import time
import hashlib
from core.db import find_similar_image, save_image_cache
from core.utils import logger

def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode('utf-8')).hexdigest()

def get_or_generate_image(prompt: str, generator_func) -> str:
    """
    generator_func: function(prompt) -> url
    """
    ph = prompt_hash(prompt)
    cached = find_similar_image(ph)
    if cached:
        logger.info("Using cached image.")
        return cached
    # else generate
    url = generator_func(prompt)
    if url:
        save_image_cache(ph, url)
    return url
