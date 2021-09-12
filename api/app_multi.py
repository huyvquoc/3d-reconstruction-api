import os

from celery import Celery
from flask_session import Session

# export PYTHONPATH=$PYTHONPATH:/media/data-huy/3D_Reconstruction/Github/openMVG/data
# os.environ['PYTHONPATH'] = '/media/data-huy/3D_Reconstruction/Github/openMVG/data'
# from extract_frames import extract_frames_from_video
# from proj3d.tasks import reconstruct_3d_model
from proj3d import factory
import proj3d


# app = Flask(__name__)
# sess = Session()
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000 * 1000
# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379', # Config Celery broker to use Redis
#     CELERY_RESULT_BACKEND='redis://localhost:6379' # Config backend to use Redis
# )

def allowed_file(filename):
    return '.' in filename and \
	    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
   app = factory.create_app(celery=proj3d.celery)
   app.secret_key = 'super secret key'
   app.config['SESSION_TYPE'] = 'filesystem'

   sess = Session()
   sess.init_app(app)

   app.debug = True
   app.run()