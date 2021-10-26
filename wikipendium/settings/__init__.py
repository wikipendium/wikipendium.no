from wikipendium.settings.base import *


try:
    from wikipendium.settings.local import *
except ImportError as e:
    raise ImportError("Failed to import local settings")
