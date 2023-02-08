from flask import Flask, render_template, request
import random
import smtplib
import ssl
import smtplib
from app_password import password
from email.message import EmailMessage
import pandas

app = Flask(__name__)

global email
global students_alums

# opening the CSV file
with open('data/students_alums.csv', mode ='r') as file:
  csvFile = pandas.read_csv(file)
students_alums = csvFile.values.tolist()
print(students_alums[0])
for i in range(len(students_alums)):
    students_alums[i] = f"{students_alums[i][1]}, {students_alums[i][2]}, {students_alums[i][3]}"
print(students_alums[0])

@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")


@app.route("/sending_code", methods=["GET","POST"])
def sending_code():
    if request.method == "GET":
        return render_template("sending_code.html")
    if request.method == "POST":
        email = request.form.get("email", default="")

        # send code (a random 6 digit number) to email
        global random_code 
        random_code = random.randint(1_000_000,9_999_999)
        print(f"random code: {random_code}")
        send_verification_code(email_receiver=email, body=str(random_code))

        return render_template("sending_code.html", email=email)


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return "Huh?"
    if request.method == "POST":
        code = int(request.form.get("code", default=""))

        if (code == random_code):
            return render_template("success_login.html", students_alums=students_alums)
        else:
            return render_template("fail_login.html")


def send_verification_code(email_receiver, body):
    # sends the emails
    email_sender = "edmuchg@gmail.com"
    email_password = password

    subject = "verify"
    body = str(random_code)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


if __name__ == '__main__':
    app.run(debug=True)
