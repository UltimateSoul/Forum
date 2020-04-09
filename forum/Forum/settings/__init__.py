import os

DEVELOPMENT = 'development'
PRODUCTION = 'production'

DEPLOYMENT_ARCHITECTURE = os.getenv('DEPLOYMENT_ARCHITECTURE', DEVELOPMENT)

if DEPLOYMENT_ARCHITECTURE == DEVELOPMENT:
    try:
        from .development import *  # noqa
    except ImportError as error:
        print("DEPLOYMENT_ARCHITECTURE: ", DEPLOYMENT_ARCHITECTURE)
        raise ImportError(
            "Nothing to import! Check {}.py file. Error: {}".format(DEVELOPMENT, error))
elif DEPLOYMENT_ARCHITECTURE == PRODUCTION:
    try:
        from .production import *  # noqa
    except ImportError as error:
        raise ImportError(
            "Nothing to import! Check {}.py file. Error: {}".format(PRODUCTION, error))