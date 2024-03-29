# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_manager.settings')

# Create a Celery instance and configure it using the settings from Django.
celery_app = Celery('expense_manager')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all installed apps.
celery_app.autodiscover_tasks()


# celery -A your_project worker -l info
