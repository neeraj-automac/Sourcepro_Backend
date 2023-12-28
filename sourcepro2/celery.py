from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

print('^^^^ in celery.py ^^^^^^^')


os.environ.setdefault('DJANGO_SETTINGS_MODULE','sourcepro2.settings')

app=Celery('sourcepro2')

app.conf.enable_utc=False

app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')


#beat settngs

app.conf.beat_schedule={
    'sending_periodically':{
        'task':'sourcepro.tasks.tes_fun',
        'schedule':timedelta(days=1),
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('-------------------------------------------------------',f'Request:{self.request!r}')
