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

    @eel.expose
    def startStudentPage(self, rfidBefore=None):
        rfid = scan(self.ser)
        if(rfidBefore != rfid):
            student = searchDb(rfid, self.queries, self.cursor)
            if student:
                recordTapDb(rfid, self.queries, self.cnx, self.cursor, student)
                print("Start!")
                return student
                # eel.updateInfo()(student)
                # sendSMS(self.ser, student)
            else:
                print("Unknown")
                # Display false
        # self.startStudentPage(rfid)

    @eel.expose
    def sendToTeacher(self, section, teacher):
        filePath = createExcelAttendance(section, self.queries, self.cursor)

        minDate, maxDate = dateRange(self.queries, self.cursor)

        subject, msg = writeEmail(section, teacher, minDate, maxDate)

        sendEmail(subject, msg, teacher, [filePath])

    @eel.expose
    def editRfidInDb(self):
        rfid = scan()
        updateDbRfid(rfid, self.queries, self.cnx, self.cursor)

    def test(self):
        self.pages.displayStudent({"id":"69","surname":"Bucas","section":"Sycip"})

arfid = Arfid("students20","tapRecords","cs","test")

# arfid.startStudentPage()
@eel.expose
def somefunction():
    print("Starting somefucntion")
    global arfid
    return arfid.startStudentPage()

# Test if these functions work
# if __name__ == "__main__":
#     global arfid
#     arfid = Arfid("students20","tapRecords","cs","test")
#     # queries, cnx, cursor, ser = initialize("students20","tapRecords","cs","test")
#
#     while(True):
#         choice = input("\nWhat do you want to test:\n"
#                        "1) Student page\n"
#                        "2) Send Email\n"
#                        "3) Edit RFID in Database\n"
#                        "[1/2/3/x]: ")
#         if(choice=="1"):
#             arfid.startStudentPage()
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