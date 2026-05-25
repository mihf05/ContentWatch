"""
Celery config for ContentWatch.
"""

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cwconfigs.settings')

app = Celery('cwconfigs')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
