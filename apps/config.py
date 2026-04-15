from pathlib import Path
import os
basedir = Path(__file__).parent.parent


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")

    
    UPLOAD_FOLDER = str(Path(basedir, "apps", "audios"))

class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True



class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    
    UPLOAD_FOLDER = str(Path(basedir, "tests", "audio_detector", "audios"))



config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}