web: gunicorn TemplateService.wsgi --bind 0.0.0.0:$PORT --log-file - --workers 3 --timeout 120
worker: celery -A TemplateService.celery worker --loglevel=info
beat: celery -A TemplateService.celery beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
release: python manage.py migrate && python manage.py collectstatic --noinput
