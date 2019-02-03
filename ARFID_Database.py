import mysql.connector
import pandas as pd

# Setup queries according to databases in use
def setupQueries(studentDatabase, tapRecordDatabase):
    global queries
    queries = {
        #Tap and Record
        "searchRfid" : "SELECT id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid FROM "+studentDatabase+" WHERE rfid = '{}'", #format with rfid; returns student info
        "recordTap" : "INSERT INTO "+tapRecordDatabase+" VALUES(0,'{}','{}', CURDATE(), CURTIME());",  #Format with studentId, rfid; records in database
        #Database to Excel
        "classList" : "SELECT classNum, surname, firstName, middleName, sex FROM "+studentDatabase+" where section='{}';",    #Format with section; returns section students
        "listDays" : "select date_format(date,'%a, %e %b') from "+tapRecordDatabase+" group by date;", #Returns dates that have tap records
        "classAttendance" : "select classNum, date_format(date,'%a, %e %b'), time_format(time, '%H:%i %p') from "+tapRecordDatabase+" " \
                             "inner join "+studentDatabase+" on "+studentDatabase+".id="+tapRecordDatabase+".studentId where "+studentDatabase+".section='{}' "
                            "group by "+tapRecordDatabase+".date, "+studentDatabase+".id;", #Format with section; returns students' tap dates and time
        #Excel to Database
        "importExcel" : "INSERT INTO "+studentDatabase+"(section, classNum, surname, firstName, middleName, gName, gNum, sex) VALUES ('{}',{},'{}','{}','{}','{}','{}','{}');",  #Format accordingly
        #Setup Database Rfid
        "searchSurname" : "select * from "+studentDatabase+" where surname='{}'", #Format with surname; returns list of people with the surname
        "updateRfid" : "update "+studentDatabase+" set rfid='{}' where id='{}'" #Format with rfid, id
    }
    return queries

# Setup database connection; resets if not; returns cursor
def setupDbCon(user, database):
    try:
        # Setup MySql connection
        global cnx, cursor
        cnx = mysql.connector.connect(user=user, database=database)
        cursor = cnx.cursor()
        print("Connected to database {}, with user {}.".format(database,user))
        return cnx, cursor
    except Exception as e:
        print(e)
        print("Retrying in 5 seconds...")
        time.sleep(5)
        checkDb(user, database)


# Search the students database for the rfid and return info or False
def searchDb(rfid):
    cursor.execute(queries.get("searchRfid").format(rfid))
    for (id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid) in cursor:
        print("{} has tapped with rfid code {}.".format(firstName, rfid))
        print("Name:", firstName, middleName, surname, "Sex:", sex)
        print("Section:", section)
        print("Class Number:", classNum, "Student ID:", id)
        if (gName != "nan" and gNum != "nan"):
            print("Contact", gName, "through", gNum)
        return id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid
    return False

# Record on the records database the studentId, date, and time of tap
def recordTapDb(rfid):
    try:
        tapper = searchDb(rfid)
        studentId = tapper[0] if tapper else None
        cursor.execute(queries["recordTap"].format(studentId, rfid))
        cnx.commit()
        print("Recorded {} - {} in database.".format(studentId, rfid))
    except Exception as e:
        print("Error in recordDb()", e)

# Update students database with the new rfid
def updateDbRfid(rfid):

    def chooseSurname():  # Checks the database for the SURNAME and returns a person's row
        surname = input("What is the SURNAME of the new owner? [Enter surname] ")
        results = []
        cursor.execute(queries["searchSurname"].format(surname))
        cursor.fetchall()
        rows = cursor.rowcount
        if (rows != 0):
            print("\n{} found.".format(rows))
            cursor.execute(queries["searchSurname"].format(surname))
            print("id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid")
            for (id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid) in cursorTemp:
                print(id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid)
                results.append((id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid))
            if (len(results) == 1):
                return results[0]
            else:
                while(True):
                    id = input("Who do you want to own the RFID Card? [Enter the id] ")
                    for result in results:
                        if (row[0] == id):
                            return result
                        else:
                            print("Invalid id, choose from the list.")
        else:
            if (input("No result found. Do you want to try again? [y/n] ") == 'y'):
                return chooseSurname()
            else:
                print("Ended.")

    def askUpdateRfid(rfid, row):  # Asks the ADMIN if s/he wants to update that row's rfid
        if(input("\nDo you want to update {} {}'s RFID Card to {}? [y/n] ".format(row[3], row[2], rfid)) == 'y'):
            try:
                cursor.execute(queries["updateRfid"].format(rfid, row[0]))
                cnx.commit()
                print("\nSuccessfully updated!")
            except Exception as e:
                print("Error occurred.\n", e)

    rfidHolder = searchDb(rfid)
    if(rfidHolder):
        print("This card is already registered to {} {} {}.".format(rfidHolder[0], rfidHolder[3], rfidHolder[2]))
        if(input("Do you want to register this card to another row? [y/n] ") == 'y'):
            row = chooseSurname()
            if(row):
                askUpdateRfid(rfid, row)
        else:
            print("Ended.")
    else:
        row = chooseSurname()
        if(row):
            askUpdateRfid(rfid, row)

# Move excel classlist to database
def importExcelToDb(filePath:str, sheetNames:list):
    for sheetName in sheetNames:
        df = pd.read_excel(filePath, sheet_name=sheetName)
        for(a,b,c,d,e,f,g,h) in zip(\
            df['Section'], df['Class Number'], df['Surname'], df['First Name'], df['Middle Name'], df['Guardian Name'], df["Guardian's Number"], df['Sex']):
            print(a,b,c,d,e,h)
            cursor.execute(queries["importExcel"].format(a,b,c,d,e,f,g,h))
    # cnx.commit() #Send the data to mysql [THIS WILL WRITE ON THE DATABASE]



# Test if these functions work
if __name__ == "__main__":
    rfid = "CE 17 8B 22"    #In place for scan()

    classList = "D:\Christiaaan's\Academic\Grade 11\Thesis\Data\School Student Roster Nov26.xlsx"

    dbUser = "cs"
    dbName = "test"

    setupQueries("students20","tapRecords")
    setupDbCon(dbUser, dbName)

    while(True):
        choice = input("\nWhat do you want to test:\n1) Record tap in database\n2) Update RFID in database\n3) Import from Excel classlist to Database\n[1/2/3/x]: ")
        if(choice == "1"): recordTapDb(rfid)
        elif(choice == "2"): updateDbRfid(rfid)
        elif(choice == "3"): importExcelToDb(classList, ['11-Hernandez', '11-Banzon', '11-Sycip'])
        else: break