from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG=None
SECRET_KEY = 'l%3ya7fn3moipdpcltj(tdfcv5^@lj=t5d&72levvls+y*@_4^'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/data'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True