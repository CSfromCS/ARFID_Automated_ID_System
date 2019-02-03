import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename

emailUser = 'upisarfid@gmail.com'
emailPass = 'JABeagle'

def sendEmail(subject: str, text: str, to: list, bcc: list, files= None, username: str= emailUser, password: str= emailPass,):
    try:
        send_from = username
        bcc = ['upisarfid@gmail.com'] if not bcc else ['upisarfid@gmail.com'] + bcc #Sends a copy to itself
        send_to = to + bcc

        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = ', '.join(to)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, "rb") as fil:
                ext = f.split('.')[-1:]
                attachedFile = MIMEApplication(fil.read(), _subtype = ext)
                attachedFile.add_header('content-disposition', 'attachment', filename=basename(f))
            msg.attach(attachedFile)

        smtp = smtplib.SMTP(host="smtp.gmail.com", port= 587)
        smtp.starttls()
        smtp.login(username,password)
        print("Logged in.")
        smtp.sendmail(send_from, send_to, msg.as_string())
        print("Email sent!")
        smtp.close()
        return True
    except Exception as e:
        print("Error in sendEmail()", e)
        return False


# Test if these functions work
if __name__ == "__main__":

    sendEmail(
    subject="Test Banzon Attendance5",
    text="Thesis test\nThis is created and sent by ARFID.\n Arf Arf!",
    to= ['magorcs@gmail.com'],  #,'brettborja@gmail.com','corojpn@gmail.com','nicolasmarew@gmail.com','dediosjoshua11@gmail.com'],
    bcc= ['upisarfid@gmail.com'],    #,'magorcs@gmail.com'],
    files= ["./Banzon_ARFID_Records_Feb 3,2019.xlsx","Hernandez_ARFID_Records_Feb 3,2019.xlsx","Sycip_ARFID_Records_Feb 3,2019.xlsx"]
    )