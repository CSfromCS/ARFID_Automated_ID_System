import eel
import time
import threading

def eelStart():
    eel.init('web')
    eel.start('data_display.html')

def initDisplay():
    eelThread = threading.Thread(target=eelStart)
    eelThread.start()

def helloMarew():
    eel.helloMarew()

def keepDisplay():
    while True:
        eel.sleep(2)

@eel.expose
def printSmt():
    print("TEST")


# def displayStudent(student):
#     eel.updateInfo(student)
#     print("Displayed!")

# Test if these functions work
if __name__ == "__main__":

    initDisplay()


    print("Hello")
    print(input("Hahsda"))
    helloMarew()

    print("Hellaao")