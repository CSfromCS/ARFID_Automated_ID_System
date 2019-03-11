import mysql.connector
import pandas as pd
import time

# Setup queries according to databases in use
def setupQueries(studentTable, tapRecordsTable, teachersTable, teacherClassesTable):
    queries = {
        #Tap and Record
        "searchRfid" : "SELECT id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid FROM "+studentTable+" WHERE rfid = '{}'", #format with rfid; returns student info
        "checkTapToday" : "SELECT * FROM taprecords WHERE rfid='{}' AND date=curdate();", #Format with rfid
        "recordTapA" : "INSERT INTO "+tapRecordsTable+"(rfid, studentId, date, time) VALUES('{}','{}', CURDATE(), CURTIME());",  #Format with rfid, studentId; records in database
        "recordTapB" : "INSERT INTO "+tapRecordsTable+"(rfid, date, time) VALUES('{}', CURDATE(), CURTIME());",  #Format with rfid; records in database
        #Message Parent
        "searchAbsents" : "SELECT id, classNum, surname, firstName, middleName, sex, section, gName, gNum, "+studentTable+".rfid, date FROM "+studentTable+" LEFT JOIN (SELECT studentId, max(date)" \
                          " AS date FROM "+tapRecordsTable+" GROUP BY studentId) AS tmp_table ON "+studentTable+".id=tmp_table.studentId WHERE date != curDate() OR date IS NULL;",
        #Database to Excel
        "classList" : "SELECT classNum, surname, firstName, middleName, sex FROM "+studentTable+" where section='{}';",    #Format with section; returns section students
        "listDays" : "SELECT date_format(date,'%a, %e %b') FROM "+tapRecordsTable+" GROUP BY date;", #Returns dates that have tap records
        "classAttendance" : "SELECT classNum, date_format(date,'%a, %e %b'), time_format(time, '%H:%i %p') FROM "+tapRecordsTable+" " \
                            "INNER JOIN "+studentTable+" ON "+studentTable+".id="+tapRecordsTable+".studentId WHERE "+studentTable+".section='{}' "
                            "GROUP BY "+tapRecordsTable+".date, "+studentTable+".id;", #Format with section; returns students' tap dates and time
        #Excel to Database
        "importExcel" : "INSERT INTO "+studentTable+"(section, classNum, surname, firstName, middleName, gName, gNum, sex, rfid) VALUES ('{}',{},'{}','{}','{}','{}','{}','{}','{}');",  #Format accordingly
        #Database to Excel
        "classRFIDList" : "SELECT rfid FROM "+studentTable+" where section='{}';", #Format with Section
        #Setup Database Rfid
        "searchSurname" : "SELECT * FROM "+studentTable+" WHERE surname LIKE '%{}%'", #Format with surname; returns list of people with the surname
        "updateRfid" : "UPDATE "+studentTable+" SET rfid='{}' WHERE id='{}';", #Format with rfid, id
        #Email queries
        "dateRange" : "SELECT DATE_FORMAT(MIN(date), '%W, %M %D, %Y'), DATE_FORMAT(MAX(date), '%W, %M %D, %Y') FROM "+tapRecordsTable+";", #Returns first and last date recorded
        "teacherList" : "(SELECT "+teacherClassesTable+".id, "+teachersTable+".name, email, class FROM "+teachersTable+" LEFT JOIN "+teacherClassesTable+" " \
                        "ON "+teachersTable+".name="+teacherClassesTable+".name where class!='NULL') UNION (SELECT "+teacherClassesTable+".id, "+teachersTable+".name, email, " \
                        "class FROM "+teachersTable+" RIGHT JOIN "+teacherClassesTable+" ON "+teachersTable+".name="+teacherClassesTable+".name where class!='NULL');", #Returns classes of teachers
        #Create Database
        "createStudentTable" : "CREATE TABLE "+studentTable+"(id int(10) NOT NULL auto_increment, classNum int(10), surname varchar(100) NOT NULL, firstName varchar(100) NOT NULL, " \
                               "middleName varchar(100), sex char(1), gName varchar(200), gNum varchar(20), section varchar(100) NOT NULL, rfid varchar(11), PRIMARY KEY(id));",
        "createTapRecordsTable" : "CREATE TABLE "+tapRecordsTable+"(tapId int NOT NULL auto_increment, studentId int(11), rfid varchar(11), date date NOT NULL, time time NOT NULL, PRIMARY KEY(tapId));",
        "createTeachersTable" : "CREATE TABLE "+teachersTable+"(id int(10) NOT NULL auto_increment, name varchar(200) NOT NULL, email varchar(100), PRIMARY KEY(id));",
        "createTeacherClassesTable" : "CREATE TABLE "+teacherClassesTable+"(id int(10) NOT NULL auto_increment, name varchar(200) NOT NULL, class varchar(50), PRIMARY KEY(id));"
    }
    return queries

# Setup database connection; resets if not; returns cursor
def setupDbCon(user, database):
    try:
        # Setup MySql connection
        cnx = mysql.connector.connect(user=user, database=database)
        cursor = cnx.cursor(buffered = True)
        print("Connected to database {}, with user {}.".format(database,user))
        return cnx, cursor
    except Exception as e:
        print(e)
        print("Retrying in 5 seconds...")
        time.sleep(5)
        return setupDbCon(user, database)

def createTables(queries, cursor, cnx):
    try:
        cursor.execute(queries["createStudentTable"])
        print("Student Table created.")
    except Exception as e:
        print(e)
    try:
        cursor.execute(queries["createTapRecordsTable"])
        print("Tap Records Table created.")
    except Exception as e:
        print(e)
    try:
        cursor.execute(queries["createTeachersTable"])
        print("Teachers Table created.")
    except Exception as e:
        print(e)
    try:
        cursor.execute(queries["createTeacherClassesTable"])
        print("Teacher Classes Table created.")
    except Exception as e:
        print(e)
    try:
        cnx.commit() #Send the data to mysql [THIS WILL WRITE ON THE DATABASE]
    except Exception as e:
        print(e)


# Search the students database for the rfid and return info or False
def searchDb(rfid, queries, cursor):
    cursor.execute(queries["searchRfid"].format(rfid))
    for (id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid) in cursor:
        print("Tapped with rfid code {}.".format(firstName, rfid))
        print("Name:", firstName, middleName, surname, "Sex:", sex)
        print("Section:", section)
        print("Class Number:", classNum, "Student ID:", id)
        if (gName != "nan" and gNum != "nan"):
            print("Contact", gName, "through", gNum)
        return id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid
    return False

def searchAbsents(queries, cursor):
    students = []
    print('{:^98}'.format("STUDENTS WHO HAVE NOT YET TAPPED TODAY."))
    print('{:^3}{:^30}{:^10}{:^12}{:^30}{:^12}'.format("Id","Name", "Section", "Last Tap", "Guardian", "Guardian Num"))

    cursor.execute(queries["searchAbsents"])
    for (id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid, date) in cursor:
        student = (id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid)
        students.append(student)
        print('{:^3}{:<30}{:^10}{:^12}{:<30}{:>11}'.format(student[0],student[2]+" "+student[3], student[6], str(date), str(student[7]), str(student[8])))
    return students if students else False

def hasTapped(rfid, queries, cursor):
    cursor.execute(queries["checkTapToday"].format(rfid))
    cursor.fetchall()
    rows = cursor.rowcount
    if (rows == 0):
        print("\n{} found.".format(rows))
        return False
    else:
        return True

# Record on the records database the studentId, date, and time of tap
def recordTapDb(rfid, queries, cnx, cursor, tapper=False):
    try:
        studentId = str(tapper[0]) if tapper else False
        if(studentId): cursor.execute(queries["recordTapA"].format(rfid, studentId))
        else:   cursor.execute(queries["recordTapB"].format(rfid))
        cnx.commit()
        print("Recorded {} - {} in database.".format(studentId if studentId else "unknown", rfid))
    except Exception as e:
        print("Error in recordTapDb()", e)

# Update students database with the new rfid
def updateDbRfid(rfid, queries, cnx, cursor):

    def chooseSurname(queries, cursor):  # Checks the database for the SURNAME and returns a person's row
        surname = input("What is the SURNAME of the new owner? [Enter surname] ")
        results = []
        cursor.execute(queries["searchSurname"].format(surname))
        cursor.fetchall()
        rows = cursor.rowcount
        if (rows != 0):
            print("\n{} found.".format(rows))
            cursor.execute(queries["searchSurname"].format(surname))
            # print("id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid")
            for (id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid) in cursor:
                print(id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid)
                results.append((id, classNum, surname, firstName, middleName, sex, section, gName, gNum, rfid))
            if (len(results) == 1):
                return results[0]
            else:
                while(True):
                    id = str(input("Who do you want to own the RFID Card? [Enter the id] "))
                    for result in results:
                        print(result[0], id)
                        if (str(result[0]) == id):
                            return result
                    else:
                        print("Invalid id, choose from the list.")
        else:
            if (input("No result found. Do you want to try again? [y/n] ") == 'y'):
                return chooseSurname(queries, cursor)
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

    rfidHolder = searchDb(rfid, queries, cursor)
    if(rfidHolder):
        print("This card is already registered to {} {} {}.".format(rfidHolder[0], rfidHolder[3], rfidHolder[2]))
        if(input("Do you want to register this card to another row? [y/n] ") == 'y'):
            row = chooseSurname(queries, cursor)
            if(row):
                askUpdateRfid(rfid, row)
        else:
            print("Ended.")
    else:
        row = chooseSurname(queries, cursor)
        if(row):
            askUpdateRfid(rfid, row)

# Move excel classlist to database
def importExcelToDb(filePath:str, sheetNames:list, queries, cursor, cnx):
    try:
        for sheetName in sheetNames:
            df = pd.read_excel(filePath, sheet_name=sheetName)
            for(a,b,c,d,e,f,g,h,i) in zip(\
                df['Section'], df['Class Number'], df['Surname'], df['First Name'], df['Middle Name'], df['Guardian Name'], df["Guardian's Number"], df['Sex'], df['RFID']):
                if 'nan' not in str(g): g = "0" + str(g)[:-2]
                # if 'nan' not in str(g):
                #     f = "Confidential"
                #     g = "+63**********"
                # else:
                #     g = "???reply???"
                #     f = g
                print('{:^10}{:^3} {:<15}{:<25}{:<15} {:<30} {:>11} {:^1} {:<11}'.format(a,b,c,d,e,f,g,h,i))
                cursor.execute(queries["importExcel"].format(a,b,c,d,e,f,g,h,i))
        cnx.commit() #Send the data to mysql [THIS WILL 3WRITE ON THE DATABASE]
    except Exception as e:
        print("Error in importExcelToDb():", e)
#Search teachers list
def returnEmailsClasses(queries, cursor):
    cursor.execute(queries["teacherList"])
    teacherClasses = {}
    teacherEmails = {}
    print(cursor)
    for (id, name, email, section) in cursor:
        teacherEmails[name] = email
        try:
            teacherClasses[name].append(section)
        except:
            teacherClasses[name] = [section]
    print (teacherClasses, teacherEmails)
    return teacherClasses, teacherEmails


# Move database data to excel
def exportDbToExcel(classList:str, sections:list, sheetNames:str, queries, cursor):
    import xlsxwriter, xlrd

    #Get old excel and rewrite
    wbRD = xlrd.open_workbook(classList)
    sheets = wbRD.sheets()

    wb = xlsxwriter.Workbook(classList)

    #Search rfid and update excel
    for sheet in sheets:  # write data from old file
        newSheet = wb.add_worksheet(sheet.name)
        for row in range(sheet.nrows):
            for col in range(sheet.ncols):
                newSheet.write(row, col, sheet.cell(row, col).value)
        if(sheet.name in sheetNames):
            i = sheetNames.index(sheet.name)
            cursor.execute(queries["classRFIDList"].format(sections[i]))
            row = 1 #Starts on row 1 since row 0 holds the header
            for (rfid,) in cursor:
                if 'nan' not in rfid:
                    newSheet.write(row, 10, rfid)
                row += 1

    wb.close()      #Writes on the excel


# Returns first and last dates of tap
def dateRange(queries, cursor):
    cursor.execute(queries["dateRange"])
    for min, max in cursor:
        print(min, max)
        return min, max



# Test if these functions work
if __name__ == "__main__":
    from ARFID_Arduino import *  #for scan()
    # ser = initArduino()

    classList = "Excel Records/School Student Roster.xlsx"

    dbUser = "cs"
    dbName = "test"

    queries = setupQueries("students20","tapRecords","teachers","teacherClasses")
    cnx, cursor = setupDbCon(dbUser, dbName)

    sections = ["Banzon", "Hernandez", "SyCip", "Faculty"]
    sheetNames = ["11-Banzon", "11-Hernandez", "11-SyCip", "Faculty"]

    while(True):
        choice = input("\nWhat do you want to test:\n1) Record tap in database\n2) Update RFID in database\n"
                       "3) Import from Excel classlist to Database\n4) Get first and last tap dates\n[1/2/3/4/5/6/7/8/x]: ")
        if(choice == "1"): recordTapDb(rfid, queries, cnx, cursor, searchDb(rfid, queries, cursor))
        elif(choice == "2"):
            rfid = scan(ser)
            updateDbRfid(rfid, queries, cnx, cursor)
        elif(choice == "3"): importExcelToDb(classList, sheetNames, queries, cursor, cnx)
        elif(choice == "4"): dateRange(queries, cursor)
        elif(choice == "5"): returnEmailsClasses(queries, cursor)
        elif(choice == "6"): exportDbToExcel(classList, sections, sheetNames, queries, cursor)
        elif(choice == "7"): createTables(queries, cursor, cnx)
        elif(choice == "8"): print(searchAbsents(queries, cursor))
        else: break