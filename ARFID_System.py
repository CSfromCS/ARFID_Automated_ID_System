from ARFID_Arduino import *
from ARFID_Database import *
from ARFID_Display import *
from ARFID_Excel import *
from ARFID_Email import *
from time

logFile = open('ARFIDLog.txt','a')

def log(message):
    logFile.write(str(datetime.datetime.now()) + " | " + message + "\n")

class Arfid():
    def __init__(self, user, database, studentTable, tapRecordsTable, teachersTable, teacherClassesTable):
        log("Starting ARFID")
        try:
            self.queries = setupQueries(studentTable, tapRecordsTable, teachersTable, teacherClassesTable)
            self.cnx, self.cursor = setupDbCon(user, database)
            self.ser = checkArduino()
            initDisplay()
            print("Done init.")
        except Exception as e:
            log("Error in Arfid.__init__(): " + str(e))

    def studentPage(self, rfid):
        try:
            self.student = searchDb(rfid, self.queries, self.cursor)

            if not self.student:
                print("Unknown")
                log("Unknown rfid {}".format(rfid))
                return False

            if hasTapped(rfid, self.queries, self.cursor):
                print("Has already tapped today")
                return (self.student, True)

            recordTapDb(rfid, self.queries, self.cnx, self.cursor, self.student)
            return (self.student, False)
        except Exception as e:
            log("Error in studentPage(): " + str(e))

    def sendToTeachers(self, sections):
        try:
            minDate, maxDate = dateRange(self.queries, self.cursor)
            teacherClasses, teacherEmails = returnEmailsClasses(self.queries, self.cursor)
            files = {}
            teacherFiles = {}
            for section in sections:
                filePath = createExcelAttendance(section, self.queries, self.cursor)
                files[section] = filePath

            for teacher in teacherClasses.keys():
                for s in teacherClasses[teacher]:
                    try:
                        teacherFiles[teacher].append(files[s])
                    except:
                        teacherFiles[teacher] = [files[s]]

                subject, msg = writeEmail(teacherClasses[teacher], teacher, minDate, maxDate)
                print(subject, msg, teacher, teacherEmails[teacher], teacherFiles[teacher])
                sendEmail(subject, msg, teacher, teacherEmails[teacher], teacherFiles[teacher])
                log("Emailed to {}:{}".format(teacher, str(teacherClasses[teacher])))
            return (True)

        except Exception as e:
            log("Error in : " + str(e))
            return (False, str(e))

    def editRfidInDb(self):
        rfid = scan(self.ser)
        updateDbRfid(rfid, self.queries, self.cnx, self.cursor)


@eel.expose
def callStudentPage(rfid):
    return arfid.studentPage(rfid)

@eel.expose
def callSendToTeachers():
    sections = ['Hernandez', 'Banzon', 'SyCip', 'Faculty']
    return arfid.sendToTeachers(sections)

@eel.expose
def callEditRfidInDb():
    return arfid.editRfidInDb()

@eel.expose
def callSendSMS():
    time.sleep(3)
    # return sendSMS(arfid.ser, arfid.student)
    print("SMS sent.")
    return False

@eel.expose
def callScan():
    return scan(arfid.ser)


arfid = Arfid("cs","test","students20","tapRecords","teachers","teacherClasses")


##Test if these functions work
# if __name__ == "__main__":
#
#     while(True):
#         # choice = '3'
#         choice = input("\nWhat do you want to test:\n"
#                        "1) Student page\n"
#                        "2) Send Email\n"
#                        "3) Edit RFID in Database\n"
#                        "[1/2/3/x]: ")
#         if(choice=="1"):
#             arfid.studentPage()
#         elif(choice=="2"):
#             arfid.sendToTeachers(sections)
#         elif(choice=="3"):
#             arfid.editRfidInDb()
#         elif(choice=="4"):
#             arfid.test()
#         else:
#             break

        # eel.sleep(3)