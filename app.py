from flask import Flask, render_template, request, session, redirect, url_for
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
    error = request.args.get('error')
    print(f"error: {error}")
    if session.get('verify') == True:
        crush_list = checkCrushList(session['email'])
        print(crush_list)
        if error is not None and error != "":
            return render_template("display_crushes.html", email=session['email'], crush_list=crush_list, error=error)
        else:
            return render_template("display_crushes.html", email=session['email'], crush_list=crush_list)
    return render_template("welcome.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # or session.pop('key', None) for specific keys
    return redirect(url_for('index'))


@app.route("/append_crush", methods=["GET", "POST"])
def append_crush():
    print(session)
    user_info = session['email']
    crush_info = request.form.get("crush", default="")
    error = add_crush(user_info, crush_info)
    crush_list = checkCrushList(session['email'])
    print(crush_list)
    return render_template("display_crushes.html", email=session['email'], crush_list=crush_list, error=error)


@app.route("/sending_code", methods=["GET", "POST"])
def sending_code():
    if request.method == "GET":
        return render_template("sending_code.html")

    if request.method == "POST":
        email = request.form.get("email", default="") + "@binghamton.edu"
        session['email'] = email

        # send code (a random 6 digit number) to email
        global random_code
        random_code = random.randint(1_000_000, 9_999_999)
        print(f"random code: {random_code}")
        send_email(subject="BU-match verify", email_receiver=email, body=str(random_code))

        return render_template("sending_code.html", email=email)


@app.route("/login", methods=["GET", "POST"])
def login():
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
    if request.method == "GET":
        if session.get('verify') is None:
            print("line80")
            return redirect(url_for('index'))
        print("line 68")
        print(session)
        # return render_template("fail_login.html")
        return render_template("add_crush.html", email=session['email'], students_alums=students_alums)


@app.route("/reveal_crush", methods=["GET", "POST"])
def reveal_crush():
    matched_crushes = checkForMatch(session['email'])
    button_crush = request.form.get("crush_reveal").split(", ")[1]
    print(f"button_crush: {button_crush}")
    if button_crush in matched_crushes:
        print(button_crush)
        print(session['email'])
        notify_both(button_crush)
        return render_template("reveal_crush.html", matched_crush=button_crush)
    return "<p>L no rizz</p>"


@app.route("/notify_both", methods=["GET", "POST"])
def notify_both(crush_email):
    email = session['email']
    # crush_email = request.form['crush_reveal']

    subject = "Match found!"
    body = "You have matched! Check the BU-match website."
    send_email(subject, email, str(body))
    send_email(subject, crush_email, body)

    error=f"Email to {crush_email} has been sent"
    return redirect(url_for('index', error=error))


def send_email(subject, email_receiver, body):
    # sends the emails
    email_sender = "edmuchg@gmail.com"
    email_password = password

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


@app.route('/delete_crush', methods=['POST'])
def delete_crush():
    crush_to_delete = request.form['crush_delete']
    email = session['email']
    print(f"my info is {email}, {crush_to_delete}")
    deleteCrush(email, crush_to_delete)
    # # print(f"session: {session}")
    # # print("line133")
    return redirect(url_for('index', error=""))


def deleteCrush(user_info, crush_info):
    # general, connection and cursor
    connection = sqlite3.connect("crushes.db")
    cursor = connection.cursor()

    # collect the list of crushes
    query = "DELETE FROM crushes WHERE self_info = ? AND crush_info = ?"
    cursor.execute(query, (user_info, crush_info))

    # commit and close
    connection.commit()
    connection.close()



def add_crush(user_info, crush_info):
    # general, connection and cursor
    connection = sqlite3.connect("crushes.db")
    cursor = connection.cursor()

    # count how many crushes the user currently has, before adding a new one
    query = f"SELECT COUNT(*) FROM crushes WHERE self_info = '{user_info}'"
    cursor.execute(query)
    crush_number = cursor.fetchone()[0]
    
    # collect the list of crushes
    python_list_crushes = checkCrushList(user_info=user_info)

    # add new crush to list
    # prevent adding if user has 5 or more crushes, or if crush is already in python_list_crushes
    error = ""
    if (crush_number < 5) and (crush_info not in python_list_crushes):
        cursor.execute(f"INSERT INTO crushes VALUES ('{user_info}', '{crush_info}')")
        python_list_crushes.append(crush_info)
    elif crush_number >= 5:
        error = "Error: You already have 5 crushes"
    elif (crush_info in python_list_crushes):
        error = f"Error: You already like {crush_info}"
    else:
        error = "Error: Bad."


    # commit and close database
    connection.commit()
    connection.close()
    print(f"after adding: {python_list_crushes}")
    return error


def checkCrushList(user_info):
    # general, connection and cursor
    connection = sqlite3.connect("crushes.db")
    cursor = connection.cursor()

    # collect the list of crushes
    query = f"SELECT crush_info FROM crushes WHERE self_info = '{user_info}'"
    cursor.execute(query)
    cursor_list = cursor.fetchall()
    crush_list = []
    for sub_list in cursor_list:
        crush_list.append(sub_list[0])
    return crush_list


def checkForMatch(user_info):
    # print(f"user_info: {user_info}")
    matched_crushes = []
    your_crushes = [i.split(",")[1].strip() for i in checkCrushList(user_info)]
    for crush in your_crushes:
        crushes_crushes = [i.split(",")[1].strip() for i in checkCrushList(crush)]
        # print(f"{crush}'s crushes: {crushes_crushes}")
        if user_info in crushes_crushes:
            # print(f"{crush} has a crush on you!")
            matched_crushes.append(crush)
    
    # print(f"matched_crushes: {matched_crushes}")
    return matched_crushes


def clear_data():
    connection = sqlite3.connect("crushes.db")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM crushes")
    connection.commit()
    connection.close()


if __name__ == '__main__':
    app.run(debug=True)


# # REST IN COMMENTS
# @app.route("/acknowledge", methods=["GET", "POST"])
# def acknowledge():
#     crush = request.form.get("crush", default="")

#     waiting = [
#         ["Nigemichi: Nashi", "_zy0sp7iZ1I"],
#         ["bluff", "CemKsp95OY4"]
#     ]
#     no_match = [
#         ["Shippai", "jTl8soYvElo"],
#         ["Souiu natsu", "udkxHDhESBI"],
#         ["Owatta", "uJ6BOG-IHN4"]
#     ]
#     match = [
#         ["Yamato nadeshiko", "FGibulARiZQ"],
#         ["Shiritsu Shuuchiin Gakuen", "Na05DCSgg2E"],
#         ["Here's your chance!", "z4wzGSgczKY"]
#     ]

#     i = 0
#     # music_url = "https://www.youtube.com/embed/" + waiting[i][1] + "?autoplay=1"
#     # music_url = "https://www.youtube.com/embed/" + no_match[i][1] + "?autoplay=1"
#     music_url = "https://www.youtube.com/embed/" + match[i][1] + "?autoplay=1"

#     print(music_url)
#     return render_template("acknowledge.html", crush=crush, music_url=music_url)