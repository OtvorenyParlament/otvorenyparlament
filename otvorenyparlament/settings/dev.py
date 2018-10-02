"""
Dev server settings
"""

from otvorenyparlament.settings.base import *

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'otvorenyparlament',
        'USER': 'otvorenyparlament',
        'PASSWORD': 'otvorenyparlament',
        'ATOMIC_REQUESTS': True,
        'HOST': 'localhost',
        'PORT': 5432
    }
}
