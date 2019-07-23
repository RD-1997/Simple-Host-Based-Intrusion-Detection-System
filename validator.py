import mysql.connector as mysql
import yaml

# loading config file for extra security
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

# initializing database connection
db = mysql.connect(
    host = cfg['mysqldb']['host'],
    user = cfg['mysqldb']['user'],
    passwd = cfg['mysqldb']['password'],
    database = cfg['mysqldb']['database']
)
cursor = db.cursor()

def validatingFiles(hash, filename):
    global authenticity     # variable used to update file authenticity in database

    # passing the passed variables into converted string variables
    passedHash = str(hash)
    passedFilename = str(filename)

    # creating query to get results of the passed file from the database
    query = "SELECT * FROM files WHERE filename = %s"
    param = (passedFilename,)
    cursor.execute(query, param)
    records = cursor.fetchall()

    # if data is not present, add it to the database
    if not records:
        # first time data will be inserted, so the file is authentic
        authenticity = "AUTHENTIC"
        # making the query SQL injection proof
        query1 = "INSERT INTO files (filename, hash, authenticity) VALUES ( %s, %s, %s)"
        param1 = (passedFilename, passedHash, authenticity)
        cursor.execute(query1, param1)
        db.commit()
        print("data added")

    else:
        # looping through columns and putting values of the file in variables
        for row in records:
         filename = row[1] # retrieves filename
         filehash = row[2] # retrieves filehash
         fileauth = row[3] # retrieves authenticity state

        # checks whether the hash is still the same, or whether it is altered.
        if filehash == passedHash:
            # if hash is unchanged, it does nothing.
            print("Everything is OK. File is authentic.")

        else:
            # if hash is changed, it updates the file authenticity state to ALTERED in the database.
            authenticity = "ALTERED"
            query2 = "UPDATE files SET authenticity = %s WHERE filename = %s"
            param2 = (authenticity, passedFilename,)
            cursor.execute(query2, param2)
            db.commit()
            print("File is altered.")


validatingFiles('m34jhwejh234', 'word.exe')