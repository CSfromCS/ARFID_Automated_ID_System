import eel
import threading

def eelStart():
    try:
        eel.init('web')
        web_app_options = {
            'mode': "chrome-app",  # or "chrome"
            'chromeFlags': ["--start-fullscreen", "--allow-file-access-from-files", '–allow-file-access-from-files']
        }
        eel.start('Index.html')#, options=web_app_options)
    except Exception as e:
        print("Error in eelStart():", e)

def initDisplay():
    eelThread = threading.Thread(target=eelStart)
    print("Initializing Display...")
    eelThread.start()



# Test if these functions work
if __name__ == "__main__":

    initDisplay()

    print("Hello")