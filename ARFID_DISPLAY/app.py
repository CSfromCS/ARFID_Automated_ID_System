from flask import Flask, render_template, request, redirect, flash, session, abort
import threading, os, subprocess
import mysql.connector

app = Flask(__name__)

config = {
	'user': 'root',
	'password': '', 
	'host': '127.0.0.1',
	'database': 'attendance_system',
	'raise_on_warnings': True
}

# assert config['password'], "hey enter db pw :)"

conn = mysql.connector.connect(**config)
cursor = conn.cursor()
logged_in = False

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		if request.form.get("page") == "admin":
			if logged_in:
				return redirect("admin")
			return redirect("login")
		elif request.form.get("page") == "student":
			return redirect("student")
	return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		if request.form.get('password') == "upis102":
			session['logged_in'] = True
			logged_in = True
			return redirect("/admin")
		else:
			error = "Wrong username/password!"
			return render_template("login.html", error=error)
	return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
	session.pop("logged_in", None)
	logged_in = False
	return redirect("/")

@app.route("/admin", methods=["GET", "POST"])
def admin():
	if request.method == "POST":
		choice = request.form.get('option')
		return redirect(choice)
	return render_template("admin.html")

@app.route("/studentroster", methods=["GET", "POST"])
def studentroster():
	if request.method == "POST":
		section = request.form.get("section")
		query = ("SELECT * FROM students WHERE section='%s'"%section)
		cursor.execute(query)
		section_list = cursor.fetchall()
		return render_template("studentroster.html", section=section, section_list=section_list)
	return render_template("studentroster.html")

@app.route("/attrecords", methods=["GET", "POST"])
def attrecords():
	return render_template("attrecords.html")

@app.route("/studentdisp", methods=["GET", "POST"])
def studentdisp():
	if request.method == "POST":
		if request.form.get("student_lname"):
			student_lname = request.form.get("student_lname")
			query = ("SELECT * FROM students WHERE surname='%s'"%student_lname)
			cursor.execute(query)
			student_data = cursor.fetchall()
			return render_template("studentdisp.html", student_data=student_data)
	return render_template("studentdisp.html")

def browserLaunch():
	CHROME = os.path.join('C://','Program Files (x86)','Google','Chrome','Application','chrome.exe')
	subprocess.call([CHROME, "--app=http://127.0.0.1:5000/"])

if __name__ == "__main__":
	threading.Timer(1, lambda: browserLaunch()).start()
	app.secret_key = os.urandom(12)
	app.run(debug=False)
