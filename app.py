from flask import Flask, render_template, request, session, redirect
import random
import smtplib
import ssl
import smtplib
from app_password import password
from email.message import EmailMessage
import pandas
from os import urandom
import sqlite3

app = Flask(__name__)
app.secret_key = urandom(32)

global email
global students_alums

# opening the CSV file
with open('data/students_alums.csv', mode='r') as file:
    csvFile = pandas.read_csv(file)
students_alums = csvFile.values.tolist()
for i in range(len(students_alums)):
    students_alums[i] = f"{students_alums[i][1]}, {students_alums[i][2]}, {students_alums[i][3]}"


@app.route("/", methods=["GET", "POST"])
def index():
    if session.get('verify') == True:
        return render_template("display_crushes.html", email=session['email'])
    return render_template("welcome.html")


@app.route("/append_crush", methods=["GET", "POST"])
def append_crush():
    print(session)
    user_info = session['email']
    crush_info = request.form.get("crush", default="")
    add_crush(user_info, crush_info)
    return render_template("display_crushes.html", email=session['email'])
    

@app.route("/sending_code", methods=["GET", "POST"])
def sending_code():
    # try:
    #     print(random_code)
    # except:
    #     return redirect("/")

    if request.method == "GET":
        return render_template("sending_code.html")

    if request.method == "POST":
        email = request.form.get("email", default="") + "@binghamton.edu"
        session['email'] = email

        # send code (a random 6 digit number) to email
        global random_code
        random_code = random.randint(1_000_000, 9_999_999)
        print(f"random code: {random_code}")
        send_verification_code(email_receiver=email, body=str(random_code))

        return render_template("sending_code.html", email=email)


@app.route("/login", methods=["GET", "POST"])
def login():
    print(session)
    if request.method == "GET":
        return render_template("add_crush.html", email=session['email'], students_alums=students_alums)
    if request.method == "POST":
        try:
            code = int(request.form.get("code", default=""))
        except:
            return render_template("fail_login.html")
        
        if (code == random_code):
            session['verify'] = True
            print(session)
            return render_template("add_crush.html", email=session['email'], students_alums=students_alums)
        else:
            return render_template("fail_login.html")


@app.route("/acknowledge", methods=["GET", "POST"])
def acknowledge():
    crush = request.form.get("crush", default="")

    waiting = [
        ["Nigemichi: Nashi", "_zy0sp7iZ1I"],
        ["bluff", "CemKsp95OY4"]
    ]
    no_match = [
        ["Shippai", "jTl8soYvElo"],
        ["Souiu natsu", "udkxHDhESBI"],
        ["Owatta", "uJ6BOG-IHN4"]
    ]
    match = [
        ["Yamato nadeshiko", "FGibulARiZQ"],
        ["Shiritsu Shuuchiin Gakuen", "Na05DCSgg2E"],
        ["Here's your chance!", "z4wzGSgczKY"]
    ]

    i = 0
    # music_url = "https://www.youtube.com/embed/" + waiting[i][1] + "?autoplay=1"
    # music_url = "https://www.youtube.com/embed/" + no_match[i][1] + "?autoplay=1"
    music_url = "https://www.youtube.com/embed/" + match[i][1] + "?autoplay=1"

    print(music_url)
    return render_template("acknowledge.html", crush=crush, music_url=music_url)


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


def add_crush(user_info, crush_info):
    # clear_data()

    print(user_info)
    print(crush_info)
    
    connection = sqlite3.connect("crushes.db")
    cursor = connection.cursor()

    # count how many crushes the user has
    query = f"SELECT COUNT(*) FROM crushes WHERE self_info = '{user_info}'"
    crush_list = cursor.execute(query)
    crush_number = cursor.fetchone()[0]
    print(f"YOU LIKE {crush_number} people")
    
    if crush_number < 5:
        cursor.execute(f"INSERT INTO crushes VALUES ('{user_info}', '{crush_info}')")
    else:
        print("You already like 5 people. No more.")

    connection.commit()
    connection.close()


def clear_data():
    connection = sqlite3.connect("crushes.db")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM crushes")
    print('We have deleted', cursor.rowcount, 'records from the table.')

    connection.commit()
    connection.close()

clear_data()

if __name__ == '__main__':
    app.run(debug=True)
