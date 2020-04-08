from .base import *

INSTALLED_APPS += [
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
]

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'elasticsearch:9200'
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.getenv('HOST'),
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'PORT': os.getenv('DB_PORT')
    }
}

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static/'),
)

CELERY_BROKER_URL = 'redis://redis:6380'
CELERY_RESULT_BACKEND = 'redis://redis:6380'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

FROM_EMAIL = os.getenv('FROM_EMAIL')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
