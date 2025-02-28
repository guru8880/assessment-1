class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    UPLOAD_FOLDER = 'uploads/'
