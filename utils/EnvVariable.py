import os
ENV = ['DB_USERNAME','DB_PASSWORD','DB_PORT','DB_HOST','DB_NAME']
class EnvVariableException(Exception):
    def __init__(self,message):
        super().__init__(message)

def checkEnvVariable():
    for evar in ENV:
        try:
            if os.environ[evar]:
                continue
        except KeyError:
            raise EnvVariableException(f"{evar} Environment Variable Not Found")
    for evar in ENV:
        if os.environ[evar] is None or os.environ[evar] == '':
            raise EnvVariableException(f"{evar} Environment Variable is None or empty")