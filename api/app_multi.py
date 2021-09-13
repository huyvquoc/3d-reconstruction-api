import os

from celery import Celery
from flask_session import Session

from proj3d import factory
import proj3d


# def allowed_file(filename):
#     return '.' in filename and \
# 	    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
   app = factory.create_app(celery=proj3d.celery)
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'

   sess = Session()
   sess.init_app(app)

   app.debug = True
   app.run()