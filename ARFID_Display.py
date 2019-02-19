import eel
import threading

def initDisplay():
    eel.init('web')
    eel.start('data_display.html', block=False)


    while True:
        eel.sleep(2)


# def displayStudent(student):
#     eel.updateInfo(student)
#     print("Displayed!")

# Test if these functions work
if __name__ == "__main__":
    pages = Pages()

    # openChrome()
    print("Hello")
    print(input("Hahsda"))
