from flask import Flask, render_template, request, redirect, session, abort
import mysql.connector
import threading, webbrowser
import os, subprocess

app = Flask(__name__)

config = {
	'user': 'root',
	'password': '10432200bcAt',
	'host': '127.0.0.1',
	'database': 'attendance_system',
	'raise_on_warnings': True
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form.get('page') == 'Admin':
			return redirect('/admin')
		elif request.form.get('page') == 'Student':
			return redirect('/student/_')
	return render_template("index.html")

@app.route("/admin", methods=['GET', 'POST'])
def admin():
	if request.method == "POST":
		password = request.form['password']
		if password == 'password':
			return redirect('/admin/section')
		else:
			return render_template("admin_login.html")
	else:
		return render_template("admin_login.html")

@app.route("/admin/section", methods=['GET', 'POST'])
def display_section():
	data = None
	section = None
	colheads = None
	if request.method == 'POST':
		section = request.form['section']
		query = ("SELECT * FROM students WHERE section='%s'"%section)
		cursor.execute(query)
		data = cursor.fetchall()

		colheads = ['ID', 'Class Number', 'Section', 'Surname', 'First Name', 'Middle Name', 'Sex', 'Guardian Name', 'Guardian Number', 'RFID']
	return render_template("admin_section.html", section=section, data=data, colheads=colheads)

@app.route("/student/<student>", methods=['GET', 'POST'])
def display_student(student=None):
	return render_template("student.html", student=student)

def browserInit():
	CHROME = os.path.join('C://','Program Files (x86)','Google','Chrome','Application','chrome.exe')
	subprocess.call([CHROME, "--app=http://127.0.0.1:5000"])

if __name__ == "__main__":
	threading.Timer(1.25, lambda: browserInit()).start()
	app.run(debug=False)



