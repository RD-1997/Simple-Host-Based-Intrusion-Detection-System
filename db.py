import mysql.connector as mysql
import yaml

# loading config file for extra security
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

# setting up connection as a function so it can be used widely
def connect():
    return mysql.connect(
        host = cfg['mysqldb']['host'],
        user = cfg['mysqldb']['user'],
        passwd = cfg['mysqldb']['password'],
        database = cfg['mysqldb']['database']
        )
