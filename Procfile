web: gunicorn TemplateService.wsgi --log-file -
worker: celery -A TemplateService.celery worker --loglevel=info
beat: celery -A TemplateService.celery beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
release: python manage.py migrate && python manage.py collectstatic --noinput
