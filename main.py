import csv


def load_users():
    with open("users.csv", "r") as file:
        reader = csv.DictReader(file)

        return list(reader)


users = load_users()

print("users: ", users)
