from ARFID_system import Arfid

arfid = Arfid("students20", "tapRecords", "cs", "test")
# queries, cnx, cursor, ser = initialize("students20","tapRecords","cs","test")

while (True):
    choice = input("\nWhat do you want to test:\n"
                   "1) Student page\n"
                   "2) Send Email\n" \
                   "3) Edit RFID in Database\n"
                   "[1/2/3/x]: ")
    if (choice == "1"):
        arfid.startStudentPage()
    elif (choice == "2"):
        section = input("Which section do you want to tally? ")
        teacher = input("Who do you want to send it to? ")

        arfid.sendToTeacher(section, teacher)
    elif (choice == "3"):
        arfid.editRfidInDb()
    else:
        break