from celery import Celery
# from flask import Flask


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