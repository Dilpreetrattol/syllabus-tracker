import time
from collections import deque, defaultdict
from functools import wraps
from flask import request, abort, current_app

# Simple in-memory rate limiter: not suitable for multi-process/production
# Keyed by (IP, endpoint)
_BUCKETS: dict[tuple[str, str], deque] = defaultdict(deque)


def rate_limit(limit: int = 5, window_seconds: int = 60):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Allow disabling via config for local debugging
            cfg = current_app.config if current_app else {}
            if cfg.get('DISABLE_RATE_LIMITS'):
                return fn(*args, **kwargs)

            ip = request.headers.get('X-Forwarded-For', request.remote_addr) or 'unknown'
            key = (ip, request.endpoint or fn.__name__)
            now = time.time()
            window = window_seconds
            q = _BUCKETS[key]

            # purge old timestamps
            while q and (now - q[0]) > window:
                q.popleft()

            if len(q) >= limit:
                # Too many requests
                abort(429)

            q.append(now)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
