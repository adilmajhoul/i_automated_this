import csv

with open("people.csv", "a", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Age", "Profession"])

    writer.writerow({"Name": "Magnus Carlsen", "Age": 29, "Profession": "King"})
