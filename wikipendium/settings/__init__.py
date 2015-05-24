from wikipendium.settings.base import *


try:
    from wikipendium.settings.local import *
except ImportError, e:
    raise ImportError("Failed to import local settings")
