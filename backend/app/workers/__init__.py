from celery import Celery
import os

celery = Celery(__name__)

def init_celery(app=None):
    """
    Initializes Celery with Flask context.
    """
    if app is None:
        from app import create_app  # 🔁 Move inside the function to delay import
        from app.config.development import DevelopmentConfig  # Adjust as needed
        app = create_app(DevelopmentConfig)

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
