"""Functions for caching per-user context."""
import hashlib
from django.core.cache import cache
from nautobot_chatops import NautobotChatOpsConfig


def _get_cache_key(user: str) -> str:
    """Key generator for the cache, adding the plugin prefix name."""
    key_string = "-".join([NautobotChatOpsConfig.name, user])
    return hashlib.md5(key_string.encode("utf-8")).hexdigest()  # nosec


def get_context(user: str) -> dict:
    """Return context stored for user."""
    return cache.get(_get_cache_key(user)) or {}


def set_context(user: str, updated_context: dict) -> None:
    """Update user context."""
    context = get_context(user)
    cache.set(_get_cache_key(user), {**context, **updated_context}, timeout=86400)
