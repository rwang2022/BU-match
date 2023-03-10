import sqlite3


def crushes_cmd(command):
    connection = sqlite3.connect("crushes.db")
    cursor = connection.cursor()
    cursor.execute(command)
    connection.commit()
    connection.close()


def clear_data():
    crushes_cmd("DELETE FROM crushes")


def deleteCrush(user_info, crush_info):
    query = f"DELETE FROM crushes WHERE self_info = {user_info} AND crush_info = {crush_info}"
    crushes_cmd(query)


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
    allow_new_crush_cond = (crush_number < 5) and (
        crush_info not in python_list_crushes)
    if allow_new_crush_cond:
        cursor.execute(
            f"INSERT INTO crushes VALUES ('{user_info}', '{crush_info}')")
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
