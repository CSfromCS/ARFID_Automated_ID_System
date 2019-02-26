from ARFID_Arduino import *
from ARFID_Database import *
from ARFID_Display import *
from ARFID_Excel import *
from ARFID_Email import *


class Arfid():
    def __init__(self, studentDatabase, tapRecordDatabase, user, database):
        self.queries = setupQueries(studentDatabase, tapRecordDatabase)
        self.cnx, self.cursor = setupDbCon(user, database)

        self.ser = checkArduino()

        initDisplay()

        print("Done init.")

    def studentPage(self):
        rfid = scan(self.ser)
        self.student = searchDb(rfid, self.queries, self.cursor)
        if self.student:
            recordTapDb(rfid, self.queries, self.cnx, self.cursor, self.student)
            return self.student
        else:
            print("Unknown")
            return False

    def sendToTeacher(self, section, teacher):
        try:
            filePath = createExcelAttendance(section, self.queries, self.cursor)

            minDate, maxDate = dateRange(self.queries, self.cursor)

            subject, msg = writeEmail(section, teacher, minDate, maxDate)

            sendEmail(subject, msg, teacher, [filePath])
            return (True)
        except Exception as e:
            return (False, e)

    def editRfidInDb(self):
        rfid = scan(self.ser)
        updateDbRfid(rfid, self.queries, self.cnx, self.cursor)



@eel.expose
def callStudentPage():
    return arfid.studentPage()

@eel.expose
def callSendToTeacher():
    return arfid.sendToTeacher()

@eel.expose
def callEditRfidInDb():
    return arfid.editRfidInDb()

@eel.expose
def callSendSMS():
    sendSMS(arfid.ser, arfid.student)


arfid = Arfid("students20","tapRecords","cs","test")


# Test if these functions work
# if __name__ == "__main__":
#     arfid = Arfid("students20","tapRecords","cs","test")
#
#     while(True):
#         choice = '3'
#         # choice = input("\nWhat do you want to test:\n"
#         #                "1) Student page\n"
#         #                "2) Send Email\n"
#         #                "3) Edit RFID in Database\n"
#         #                "[1/2/3/x]: ")
#         if(choice=="1"):
#             arfid.studentPage()
#         elif(choice=="2"):
#             section = input("Which section do you want to tally? ")
#             teacher = input("Who do you want to send it to? ")
#
#             arfid.sendToTeacher(section, teacher)
#         elif(choice=="3"):
#             arfid.editRfidInDb()
#         elif(choice=="4"):
#             arfid.test()
#         else:
#             break
#
#         eel.sleep(3)