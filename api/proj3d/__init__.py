from celery import Celery
# from flask import Flask


# def make_celery(app):
#     celery = Celery(
#         app, # or 'proj3d'
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL'],
#         include=['proj3d.tasks']
#     )
#     celery.conf.update(app.config)

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery

# flask_app = Flask(__name__)
# flask_app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379', # Config Celery broker to use Redis
#     CELERY_RESULT_BACKEND='redis://localhost:6379' # Config backend to use Redis
# )
# app = make_celery(flask_app) # create celery application

def make_celery(app=__name__):
    redis_url = 'redis://localhost:6379'
    celery = Celery(
        'proj3d',
        backend=redis_url,
        broker=redis_url,
        include=['proj3d.tasks']
    )
    return celery

celery = make_celery()