import time

# importing our db.py
import db

# initializing db connection
conn = db.connect()
cursor = conn.cursor()

# function to validate the incoming files from the host
def manageFiles(hash, filename, scanner):
    # variable used to update file authenticity in database
    global state

    # passing the passed variables into converted string variables
    passedHash = str(hash)
    passedFilename = str(filename)
    passedScanner = str(scanner)

    # defining the last scan time
    scantime = time.strftime('%Y-%m-%d %H:%M:%S')

    # creating query to get results of the passed file from the database
    query = "SELECT * FROM files WHERE filename = %s"
    param = (passedFilename,)
    cursor.execute(query, param)
    records = cursor.fetchall()

    # if data is not present, add it to the database
    if not records:

        state = "unchanged"
        # making the query SQL injection proof
        query1 = "INSERT INTO files (scanner, filename, original_hash, time_added, last_scan, state) VALUES ( %s, %s, %s, %s, %s, %s)"
        param1 = (passedScanner, passedFilename, passedHash, scantime, scantime, state)

        # puts the query and parameters together and executes it
        cursor.execute(query1, param1)

        # commit is necessary for the changes to be applied and saved in the database
        conn.commit()
        print("New file detected! Data added to database")

    # if data is present in database do following:
    else:
        # scanning through columns and putting values of the file in variables
        for row in records:
         filehash = row[3]  # retrieves filehash

        # checks whether the hash is still the same, or whether it is altered.
        if filehash == passedHash:

            # the reason why the state will be set to unchanged is when a changed file is fixed it will be
            # recovered to it's original state, and therefore the relevant columns will be cleared in the db
            state = "unchanged"
            discoveryTime = None
            changedHash = None

            # if the hash is still the same, then just update the last scan
            query2 = "UPDATE files SET last_scan = %s, state = %s, changed_hash = %s, time_of_alteration = %s WHERE filename = %s AND scanner = %s"
            param2 = (scantime, state, discoveryTime, changedHash, passedFilename, passedScanner)

            # puts the query and parameters together and executes it
            cursor.execute(query2, param2)

            # commit is necessary for the changes to be applied and saved in the database
            conn.commit()

            print("Nothing to see here! File is in original state.")

        # if file is changed
        else:
            # simple check to see whether file already has been identified as changed
            query3 = "SELECT time_of_alteration FROM files WHERE filename = %s AND scanner = %s"
            param3 = (passedFilename, passedScanner)
            cursor.execute(query3, param3)
            records3 = cursor.fetchone()

            # if file is not yet classified as changed, it will update the following values
            if not records3[0]:
                # if hash is changed, it updates the file authenticity state to ALTERED in the database.
                state = "changed"

                # making the query SQL injection proof
                query4 = "UPDATE files SET last_scan = %s, state = %s, changed_hash = %s, time_of_alteration = %s WHERE filename = %s AND scanner = %s"

                param4 = (scantime, state, passedHash, scantime, passedFilename, scanner)

                # puts the query and parameters together and executes it
                cursor.execute(query4, param4)

                # commit is necessary for the changes to be applied and saved in the database
                conn.commit()

                print("File is changed! That does not look good. Updating details in db.")

            # if file is already registered as altered, it only updates the last scan time
            else:
                # making the query SQL injection proof
                query5 = "UPDATE files SET last_scan = %s WHERE filename = %s AND scanner = %s"

                param5 = (scantime, passedFilename, passedScanner)

                # puts the query and parameters together and executes it
                cursor.execute(query5, param5)

                # commit is necessary for the changes to be applied and saved in the database
                conn.commit()

                print("Updating latest scan time for an already changed file.")
