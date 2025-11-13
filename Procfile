web: gunicorn TemplateService.wsgi --bind 0.0.0.0:8080 --log-file - --workers 3  --timeout 300 --keep-alive 75 --max-requests 1000 --max-requests-jitter 100
worker: celery -A TemplateService.celery worker --loglevel=info
beat: celery -A TemplateService.celery beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
release: python manage.py collectstatic --noinput
