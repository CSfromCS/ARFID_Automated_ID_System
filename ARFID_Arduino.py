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
        print("Connected to arduino rfid and sim module through port {}.".format(arduino_ports[0]))
        return True
    except Exception as e:
        print(e)
        print("Retrying in 5 seconds...")
        time.sleep(5)
        checkArduino()

# Wait for an rfid card and return its UID
def scan():
    return input("RFID UID: ")  #Temporary, while I don't have an arduino at hand

# Instruct Arduino to send an SMS message to guardian
def sendSMS(firstName, gName, gNum, date, time):
    print("Message sent!")
    pass



# Test if these functions work
if __name__ == "__main__":
    if (checkArduino()):
        print("Arduino found!")

        rfid = scan()
        print(rfid,"tapped!")

        sendSMS("Test Student", "Test Guardian", "09178024116", "Date Here", "Time Here")
    else:
        print("Arduino not found")