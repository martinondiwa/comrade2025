from celery import Celery
from backend.app import create_app
from backend.app.config.development import DevelopmentConfig  # Adjust as per your env

celery = Celery(
    __name__,
    broker=DevelopmentConfig.CELERY_BROKER_URL,
    backend=DevelopmentConfig.CELERY_RESULT_BACKEND
)

def init_celery(app=None):
    """
    Initialize Celery with Flask app context.
    """
    app = app or create_app(DevelopmentConfig)
    celery.conf.update(app.config)

    # Flask context wrapped around each task
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
