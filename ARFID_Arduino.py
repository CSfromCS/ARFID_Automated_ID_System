import serial
import serial.tools.list_ports
import time

# Checks if the Arduino rfid scanner and sim module is active; resets arduino if not
def checkArduino():
    try:
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'Arduino' in p.description
        ]

        ser = serial.Serial(arduino_ports[0], 9600)
        print("Connected to arduino through port '{}'.".format(arduino_ports[0]))

        ser.write(b'0\n')

        while (True):
            ser.write(b'1\n')
            fromArduino = readSerial(ser)
            if("Ready" in fromArduino):
                print("Rfid scanner ready.")
                break

        while (True):
            ser.write(b'2\n')    #I dont have sim yet
            fromArduino = readSerial(ser)
            if("Ready" in fromArduino):
                print("GSM ready.")
                break

        print("Connected to rfid and sim module through port '{}'.".format(arduino_ports[0]))

        return ser
    except Exception as e:
        print(e)
        print("Retrying in 5 seconds...")
        time.sleep(5)
        return checkArduino()

def readSerial(ser):
    line = str(ser.readline())[2:-5]
    return line

# Wait for an rfid card and return its UID
def scan(ser):
    ser.write(b'3\n')
    print("\nScanning...\n")
    line = ""
    while("UID" not in line):
        line = readSerial(ser)
        print(line)
    ser.write(b'x\n')
    return line[5:]
    # return input("RFID UID: ")  #Temporary, while I don't have an arduino at hand

# Instruct Arduino to send an SMS message to guardian
def sendSMS(ser, student):
    print("Sending message...")
    ser.write(b'4\n')
    time.sleep(0.2)
    ser.write(bytes(student[8]+'\n', 'utf-8'))
    time.sleep(0.1)
    ser.write(bytes("{}, THIS IS SENT BY ARFID\n".format(student[7]), 'utf-8'))
    while("COMPLETE" not in readSerial(ser)): pass
    print("Message sent!")



# Test if these functions work
if __name__ == "__main__":
    ser = checkArduino()
    if (ser):
        print("Arduino found!")

        rfid = scan(ser)
        print(rfid,"tapped!")

        sampleStudent = ("92", "42", "Nicolas", "Marew", "Cruz", "F", "Banzon", "Jorbeagle", "09276311408", "DE AD BE EF")

        sendSMS(ser, sampleStudent)
    else:
        print("Arduino not found")