import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','myshop.settings')
app = Celery('myshop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#celery -A myshop worker -l info ----> Start a worker
#rabbitmq-server ---- start message broker for celery
# flower for monitoring celery workers