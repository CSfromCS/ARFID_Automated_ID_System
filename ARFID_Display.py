from flask import Flask, render_template
# from flask.ext.socketio import SocketIO, emit
from datetime import datetime
import threading

class Pages():
    app = Flask(__name__)
    def __init__(self):
        threading.Thread(target=Pages.app.run).start()
        # app.config['SECRET_KEY'] = 'secret!'
        # socketio = SocketIO(app)

    @app.route("/")
    def home():
        return render_template("HOME.html")

    @app.route("/sign_in")
    def sign_in():
        return render_template("SIGNIN.html")

    @app.route("/wait")
    def wait():
        return render_template("WAIT.html")

    studentData = {"id":"69","surname":"Bucas","section":"Sycip"}

    @app.route("/student")
    def displayStudent(self, studentData):
        return render_template("STUDENT.html", student=studentData, time=datetime.now().strftime('%I:%M %p'),
                               date=datetime.now().strftime('%A, %B %d, %Y'))

    # @app.route("/student", methods = ['POST'])
    # def student():
    #     data = request.get_json()
    #     result = ''
    #
    #     for item in data:
    #         # loop over every row
    #         result += str(item['make']) + '\n'
    #
    #     return result

    # Send info to Javascript and display to HTML
    def displayJS():
        pass

    def openChrome():
        import webbrowser
        url = "https://localhost:5000"
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)
        print("browser opened")

# Test if these functions work
if __name__ == "__main__":
    pages = Pages()

    # openChrome()
    print("Hello")
    print(input("Hahsda"))
