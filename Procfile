release: python manage.py collectstatic --noinput
web: gunicorn TemplateService.wsgi
# worker: celery -A TemplateService worker --loglevel=info
# beat: celery -A TemplateService beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
