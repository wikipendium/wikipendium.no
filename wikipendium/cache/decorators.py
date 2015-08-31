from django.core.cache import caches


def _make_cache_key_from_function(fn, *args, **kwargs):
    return '%s.%s(%s,%s)' % (
        fn.__module__,
        fn.__name__,
        '(args:%s)' % ','.join(map(str, map(hash, args))),
        '(kwargs:%s)' % ','.join(map(str, map(hash, kwargs.items()))),
    )


def cache_page_per_user(fn, *args, **kwargs):
    def key(request, *args, **kwargs):
        return (_make_cache_key_from_function(fn, *args, **kwargs) +
                'user(pk=%s, username=%s)' % (
                    request.user.pk
                    if request.user.is_authenticated()
                    else 'None', request.user.username))

    return cache(fn, key)


def cache_model_method(fn):
    def key(self, *args, **kwargs):
        return (_make_cache_key_from_function(fn, *args, **kwargs) +
                '%s(pk=%s)' % (type(self).__name__, self.pk))
    return cache(fn, key)


def cache(fn, key=None):
    cache = caches['default']

    def inner(*args, **kwargs):
        if key is None:
            cache_key = _make_cache_key_from_function(fn, *args, **kwargs)
        elif hasattr(key, '__call__'):
            cache_key = key(*args, **kwargs)
        else:
            cache_key = str(key)
        cached = cache.get(cache_key)
        if cached:
            return cached
        result = fn(*args, **kwargs)
        cache.set(cache_key, result)
        return result
    return inner
