web: gunicorn TemplateService.wsgi --bind 0.0.0.0:8080 --log-file - --workers 1
release: python manage.py collectstatic --noinput
