from flask import Flask, render_template, request, redirect, url_for
import cv2
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Users stored in program
users = {
    "karthik": {"password": "2005", "role": "faculty"},
    "nikola": {"password": "1234", "role": "student"}
}

# -------- Attendance Function --------
def mark_attendance(name, period):

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    filename = f"attendance_{date}_{period}.csv"

    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=["Name","Time","Period"])

    if name not in df["Name"].values:
        new_row = {"Name":name,"Time":time,"Period":period}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_csv(filename,index=False)


# -------- Home --------
@app.route('/')
def home():
    return render_template('login.html')


# -------- Login --------
@app.route('/login', methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']

    if username in users and users[username]["password"] == password:

        role = users[username]["role"]

        if role == "faculty":
            return redirect(url_for('faculty_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))

    return "Invalid Username or Password"


# -------- Faculty Page --------
@app.route('/faculty')
def faculty_dashboard():
    return render_template("faculty.html")


# -------- Student Page --------
@app.route('/student')
def student_dashboard():
    return "<h1>Student Dashboard</h1><br>View Your Attendance Here"


# -------- Upload Image & Detect Faces --------
@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['image']

    if file.filename == "":
        return "No file selected"

    filepath = "class.jpg"
    file.save(filepath)

    period = "P1"

    img = cv2.imread(filepath)

    if img is None:
        return "Image could not be read"

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    print("Faces detected:", len(faces))

    if len(faces) == 0:
        return "No faces detected in the image"

    for (x,y,w,h) in faces:
        name = "Student"
        mark_attendance(name, period)

    return render_template("success.html")

# -------- Run Server --------
if __name__ == "__main__":
    app.run(debug=True)