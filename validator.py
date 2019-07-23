import time

# importing our db.py
import db

# initializing db connection
conn = db.connect()
cursor = conn.cursor()

# function to validate the incoming files from the host
def validatingFiles(hash, filename):
    # variable used to update file authenticity in database
    global authenticity

    # passing the passed variables into converted string variables
    passedHash = str(hash)
    passedFilename = str(filename)

    # defining the last scan time
    scantime = time.strftime('%Y-%m-%d %H:%M:%S')

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
        query1 = "INSERT INTO files (filename, hash, authenticity, lastscan) VALUES ( %s, %s, %s, %s)"
        param1 = (passedFilename, passedHash, authenticity, scantime)

        # puts the query and parameters together and executes it
        cursor.execute(query1, param1)

        # commit is necessary for the changes to be applied and saved in the database
        conn.commit()
        print("data added")

    # if data is present in database do following:
    else:
        # scanning through columns and putting values of the file in variables
        for row in records:
         filename = row[1] # retrieves filename
         filehash = row[2] # retrieves filehash
         fileauth = row[3] # retrieves authenticity state

        # checks whether the hash is still the same, or whether it is altered.
        if filehash == passedHash:

            # if the hash is still the same, then just just update the last scan time
            query2 = "UPDATE files SET lastscan = %s WHERE filename = %s"
            param2 = (scantime, passedFilename,)

            # puts the query and parameters together and executes it
            cursor.execute(query2, param2)

            # commit is necessary for the changes to be applied and saved in the database
            conn.commit()

            print("Everything is OK. File is authentic.")

        else:
            # if hash is changed, it updates the file authenticity state to ALTERED in the database.
            authenticity = "ALTERED"

            # making the query SQL injection proof
            query3 = "UPDATE files SET authenticity = %s, lastscan = %s WHERE filename = %s"
            param3 = (authenticity, scantime, passedFilename,)

            # puts the query and parameters together and executes it
            cursor.execute(query3, param3)

            # commit is necessary for the changes to be applied and saved in the database
            conn.commit()
            print("File is altered. That does not look good.")

