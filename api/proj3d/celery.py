import os
import subprocess
import time
import datetime
import zipfile

from celery import Celery
from flask import Flask

from extract_frames import extract_frames_from_video

def make_celery(app):
    celery = Celery(
        'proj3d',
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['proj3d.tasks']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Add two numbers together
flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379', # Config Celery broker to use Redis
    CELERY_RESULT_BACKEND='redis://localhost:6379' # Config backend to use Redis
)
app = make_celery(flask_app) # create celery application

# app = Celery('proj3d',
#              broker='redis://',
#              backend='redis://',
#              include=['proj3d.tasks'])

# Optional configuration, see the application user guide.
# app.conf.update(
#     result_expires=3600,
# )

if __name__ == '__main__':
    app.start()