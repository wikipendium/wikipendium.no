from wikipendium.settings.base import *


try:
    from wikipendium.settings.local import *
except ImportError, e:
    raise ImportError("Failed to import local settings")


from django.conf.global_settings import (
    AUTHENTICATION_BACKENDS as DEFAULT_AUTHENTICATION_BACKENDS
)

try:
    if DEBUG and ACTIVATE_FAKEAUTH == "YES, I WANT TO ENABLE PASSWORDLESS LOGIN" \
            + " FOR ALL USERS, INCLUDING SUPERUSERS":
        AUTHENTICATION_BACKENDS = DEFAULT_AUTHENTICATION_BACKENDS + \
            ('wikipendium.fakeauth.FakeAuthBackend',)
except NameError:
    pass
