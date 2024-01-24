# Creates CSV file and generates password


import csv
import os


def generate_password():
    password = os.popen('mkpasswd -l 12 -c 4 -C 4 -d 4 -s 0').read()
    return password


def main():
    file = "liste-etudiants.csv"
    with open(file, newline='') as list:
        student_list = csv.reader(list, delimiter=";")
        for count, line in enumerate(student_list):
            name = line[0]
            firstname = line[1]
            group = line[2]
            category = line[2][1].lower()

            student_id = f"{category}{count + 1:04d}"

            password = generate_password()

            user = f"{name};{firstname};{group};{student_id};{password}".rstrip()
            print(user)


if __name__ == '__main__':
    main()
