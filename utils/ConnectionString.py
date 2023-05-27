import os
from utils.EnvVariable import ENV
def getConsString():
    DB_USERNAME = os.environ[ENV[0]]
    DB_PASSWORD = os.environ[ENV[1]] 
    DB_PORT = os.environ[ENV[2]]
    DB_HOST = os.environ[ENV[3]]
    DB_NAME = os.environ[ENV[4]]
    return f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"