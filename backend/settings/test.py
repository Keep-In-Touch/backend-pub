import sys

from backend.settings.main import *

DEBUG = False
TEMPLATE_DEBUG = False
TEST = True

# ----------------------------------------
# Django settings.
# ----------------------------------------
PASSWORD_HASHERS = (  # Use md5 password hasher to speedup tests
    "django.contrib.auth.hashers.MD5PasswordHasher",
)


# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

# ----------------------------------------
# Databases setup
# ----------------------------------------


if "--sqlite" in sys.argv:
    print("Using SQLITE for testing")
    DATABASES["default"] = {"ENGINE": "django.db.backends.sqlite3"}
# else:
#     print("Using PostgreSQL for testing")
#     DATABASES["default"] = {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "ncloudsken",
#         "USER": "root",
#         "PASSWORD": "",
#         "MIGRATE": False,
#         "HOST": "mysql",
#         "PORT": "3306",
#         "OPTIONS": {"init_command": "SET storage_engine=MyISAM"},
#     }
