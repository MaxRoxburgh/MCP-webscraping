import diskcache as dc
import hashlib

cache = dc.Cache('./gemini_cache')

def get_cache_key(prompt, params=None):
    key_data = prompt + str(params)
    return hashlib.sha256(key_data.encode()).hexdigest()