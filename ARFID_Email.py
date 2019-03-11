import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

emailUser = 'upisarfid@gmail.com'
emailPass = 'JABeagle'

def writeEmail(sections, teacher, minDate, maxDate):
    subjectSection = ""
    listSection = ""
    for section in sections:
        subjectSection += section + " "
        listSection += section + "\n"

    msg = "\n"+teacher+"\n\nHere are the attendance records of:\n\n{}\nfrom {} to {}.\n".format(listSection, minDate, maxDate)
    msg += "\n______________________________________________________________\nThis automated message is created and sent by ARFID. ARFID is an automated RFID-based attendance system that records "\
           "\nand tallies attendance to provide efficient and accurate records. For any concerns, please email: upisarfid@gmail.com"

    subject = "ARFID: {}Attendance Record".format(subjectSection)

    return subject, msg

def sendEmail(subject: str, text: str, to: str, toEmail: str, files= None, bcc: list= None, username: str= emailUser, password: str= emailPass,):
    try:
        send_from = username
        bcc = ['upisarfid@gmail.com'] if not bcc else ['upisarfid@gmail.com'] + bcc #Sends a copy to itself
        to = toEmail

        send_to = bcc + [to]

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        print("Message: {}".format(msg.as_string()))

        for f in files or []:
            with open(f, "rb") as fil:
                ext = f.split('.')[-1:]
                attachedFile = MIMEApplication(fil.read(), _subtype = ext)
                attachedFile.add_header('content-disposition', 'attachment', filename=basename(f))
            msg.attach(attachedFile)

        smtp = smtplib.SMTP(host="smtp.gmail.com", port= 587)
        try:
            smtp.starttls()
            smtp.login(username,password)
            print("Logged in.")
            # smtp.sendmail(send_from, send_to, msg.as_string())
            print("Email sent!")
            return True
        except Exception as f:
            print("Error in sendEmail()*", f)
            return False
        finally:
            smtp.close()
    except Exception as e:
        print("Error in sendEmail()", e)
        return False



# Test if these functions work
if __name__ == "__main__":
    from ARFID_Database import *

    dbUser = "cs"
    dbName = "test"

    queries = setupQueries("students20", "tapRecords","teachers","teacherClasses")
    cnx, cursor = setupDbCon(dbUser, dbName)

    min, max = dateRange(queries, cursor)

    section = ["Banzon"]
    teacher = "Sarabia, C."
    sectionFile = "Excel Records/Banzon_ARFID_Records_Feb4,2019.xlsx"

    subject, msg = writeEmail(section, teacher, min, max)
    print(subject, msg)

    # sendEmail(
    #     subject= subject,
    #     text= msg,
    #     to= teacher,  #,'brettborja@gmail.com','corojpn@gmail.com','nicolasmarew@gmail.com','dediosjoshua11@gmail.com'],
    #     # bcc= []    #,'magorcs@gmail.com'],
    #     files= [sectionFile]
    # )