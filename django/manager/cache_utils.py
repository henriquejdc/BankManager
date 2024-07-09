import json

from django.core.cache import cache

from bank_manager import settings


def set_cache(key, value, timeout=None):
    """
    Sets a value in the cache.
    :param key: The key to identify the value in the cache.
    :param value: The value to be stored in the cache. Can be a dictionary.
    :param timeout: Time in seconds before the cache expires. If None, uses the default.
    """
    if isinstance(value, dict):
        value = json.dumps(value)
    cache.set(f'{settings.REDIS_CACHE_KEY_PREFIX}_{key}', value, timeout)


def get_cache(key):
    """
    Retrieves a value from the cache.
    :param key: The key to identify the value in the cache.
    :return: The value stored in the cache or None if the key does not exist.
    """
    value = cache.get(f'{settings.REDIS_CACHE_KEY_PREFIX}_{key}')
    try:
        value = json.loads(value)
    except (TypeError, json.JSONDecodeError):
        pass
    return value
