import os

DEVELOPMENT = 'development'
PRODUCTION = 'production'

DEPLOYMENT_ARCHITECTURE = os.getenv('DEPLOYMENT_ARCHITECTURE', DEVELOPMENT)

if DEPLOYMENT_ARCHITECTURE == DEVELOPMENT:
    try:
        from .development import *
    except ImportError as error:
        raise ImportError(
            "Nothing to import! Check {}.py file".format(DEVELOPMENT))
elif DEPLOYMENT_ARCHITECTURE == PRODUCTION:
    try:
        from .production import *
    except ImportError as error:
        raise ImportError(
            "Nothing to import! Check {}.py file".format(PRODUCTION))