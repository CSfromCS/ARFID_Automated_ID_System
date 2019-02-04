from ARFID_Arduino import *
from ARFID_Database import *
from ARFID_Display import *
from ARFID_Excel import *
from ARFID_Email import *

# print(ARFID_Arduino, ARFID_Database, ARFID_Display, ARFID_Excel, ARFID_Email)

def initialize(studentDatabase, tapRecordDatabase, user, database):
    queries = setupQueries(studentDatabase, tapRecordDatabase)
    cnx, cursor = setupDbCon(user, database)

    # checkArduino()

    return queries, cnx, cursor

def startStudentPage():
    rfid = scan()
    student = searchDb(rfid)
    if student:
        recordTapDb(rfid, student)
        #Display
    else:
        #Display false
        pass

def sendToTeacher(section, teacher, queries, cursor):
    filePath = createExcelAttendance(section, queries, cursor)

    minDate, maxDate = dateRange()

    subject, msg = writeEmail(section, teacher, minDate, maxDate)

    sendEmail(subject, msg, teacher, [filePath])

def editRfidInDb():
    rfid = scan()
    updateDbRfid(rfid)



# Test if these functions work
if __name__ == "__main__":
    queries, cnx, cursor = initialize("students20","tapRecords","cs","test")

    while(True):
        choice = input("\nWhat do you want to test:\n"
                       "1) Student page\n"
                       "2) Send Email\n" \
                       "3) Edit RFID in Database\n"
                       "[1/2/3/x]: ")
        if(choice=="1"):
            startStudentPage()
        elif(choice=="2"):
            section = input("Which section do you want to tally? ")
            teacher = input("Who do you want to send it to? ")

            sendToTeacher(section, teacher, queries, cursor)
        elif(choice=="3"):
            editRfidInDb()
        else:
            break