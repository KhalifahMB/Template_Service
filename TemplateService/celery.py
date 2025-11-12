import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TemplateService.settings')

# Name the Celery app after the Django project package for clarity.
app = Celery('TemplateService')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'warm-template-cache-every-30-minutes': {
        'task': 'notification_templates.tasks.warm_template_cache',
        'schedule': 1800.0,  # 30 minutes in seconds
        'options': {
            'expires': 15.0,
        },
    },
    'cleanup-old-render-logs-daily': {
        'task': 'notification_templates.tasks.cleanup_old_render_logs',
        'schedule': 86400.0,  # 24 hours in seconds
        'kwargs': {'days': 30},  # Keep logs for 30 days
    },
    'health-check-hourly': {
        'task': 'notification_templates.tasks.health_check',
        'schedule': 3600.0,  # 1 hour in seconds
    },
}

app.conf.timezone = 'UTC'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
