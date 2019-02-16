import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

emailUser = 'upisarfid@gmail.com'
emailPass = 'JABeagle'

teachers = {
    "Pineda, L." : {"name" : "Ms. Laurice A. Pineda",
                    "email" : "lapineda@up.edu.ph"},
    "Guerrero, C." : {"name" : "Prof. Charlaine G. Guerrero",
                      "email" : "cgguerrero@up.edu.ph"},
    "Macapagal, M." : {"name" : "Mr. Molave Nemesio C. Macapagal",
                       "email" : "mcmacapagal2@up.edu.ph"},
    "Prieto, C." : {"name" : "Bb. Mary Christine C. Prieto",
                    "email" : "mcprieto@up.edu.ph"},
    "Baygan, M." : {"name" : "Ms. Maria Araceli M. Baygan",
                    "email" : ""},  #Email
    "Ereno, R." : {"name" : "Prof. Rhodora F. Ereno",
                   "email" : ""},   #Email
    "Velasquez, R." : {"name" : "Prof. Roselle J. Velasquez",
                       "email" : ""},   #Email
    "Taduran, R." : {"name" : "Prof. Regina Carla R. Taduran",
                     "email" : "rrtaduran@up.edu.ph"},
    "Vargas, M." : {"name" : "Prof. Ma. Lourdes J. Vargas",
                    "email" : "vargasdet@gmail.com"},
    "Sarabia, C." : {"name" : "Christian Sarabia",
                     "email" : "magorcs@gmail.com"}
}

def writeEmail(section, teacher, minDate, maxDate):
    subject = "ARFID: " + section + " Attendance Record"

    msg = teachers[teacher]["name"] + "\n\nHere is the attendance record of {} from {} to {}.\n".format(section, minDate, maxDate)
    msg += "\n______________________________________________________________\nThis message is created and sent by ARFID. ARFID is an automated RFID-based attendance system that records and tallies " \
           "attendance to provide efficiency and accuracy. For any concerns, please email: upisarfid@gmail.com"
    return subject, msg

def sendEmail(subject: str, text: str, to: str, bcc: list= None, files= None, username: str= emailUser, password: str= emailPass,):
    try:
        send_from = username
        bcc = ['upisarfid@gmail.com'] if not bcc else ['upisarfid@gmail.com'] + bcc #Sends a copy to itself
        to = teachers[to]["email"]

        send_to = bcc + [to]

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = to
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

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
            print("Message: {}".format(msg.as_string()))
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

    queries = setupQueries("students20", "tapRecords")
    cnx, cursor = setupDbCon(dbUser, dbName)

    min, max = dateRange()

    section = "Banzon"
    teacher = "Sarabia, C."
    sectionFile = "Excel Records/Banzon_ARFID_Records_Feb4,2019.xlsx"

    subject, msg = writeEmail(section, teacher, min, max)

    sendEmail(
        subject= subject,
        text= msg,
        to= teacher,  #,'brettborja@gmail.com','corojpn@gmail.com','nicolasmarew@gmail.com','dediosjoshua11@gmail.com'],
        # bcc= []    #,'magorcs@gmail.com'],
        files= [sectionFile]
    )