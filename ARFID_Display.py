import eel
import sys
import threading

def eelStart():
    eel.init('web')
    eel.start('Student.html')

def initDisplay():
    eelThread = threading.Thread(target=eelStart)
    eelThread.start()


# Test if these functions work
if __name__ == "__main__":

    initDisplay()


    print("Hello")
    print(input("Hahsda"))
    helloMarew()

    print("Hellaao")