import json
import pandas

# loading data from file 
f = open("json.txt", "r")
x = f.read()
# a person is represented by a dictionary (name, BU_email, and job_title)
# list of dictionaries of everyone
list_of_everyone = json.loads(x)

# filters a list of dictionaries, of only students and alums
included = ["ALUM, Binghamton University", "STUDENT, Binghamton University"]
students_alums = [{key:value for (key,value) in person.items()} for person in list_of_everyone if person["job_title"] in included]
unsure = [{key:value for (key,value) in person.items()} for person in list_of_everyone if person["job_title"] == ""]

# printing to make sure
print(f"everyone: {len(list_of_everyone)}\nstudents_alums: {len(students_alums)}\nunsure: {len(unsure)}")
print(students_alums[100].items())
print(unsure[100].items())

# exporting to csv
df = pandas.DataFrame(students_alums)
df.to_csv("../data/students_alums.csv")

df = pandas.DataFrame(unsure)
df.to_csv("../data/unsure.csv")