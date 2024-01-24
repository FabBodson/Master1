import csv
import os


def create_local_group(group):
    return os.popen(f'groupadd {group}').read()


def create_local_user(name, firstname, group, student_id, password):
    return os.popen(f'useradd -m -g users -G {group} -p {password} -c "{firstname} {name}" {student_id}').read()


def main():
    file = "liste-login-pass.csv"
    counter = 0
    with open(file, newline='') as list:
        student_list = csv.reader(list, delimiter=";")

        for line in student_list:
            name = line[0]
            firstname = line[1]
            group = line[2].lower()
            student_id = line[3]
            password = line[4]

            create_local_group(group)

            create_local_user(name, firstname, group, student_id, password)

            user = f"{name};{firstname};{group};{student_id};{password}".rstrip()
            print(user)

            if counter == 3:
                break
            else:
                counter += 1


if __name__ == '__main__':
    main()
