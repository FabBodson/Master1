import csv
import os
import sys


def create_global_user(name, firstname, uid_number, login, password, file_to_write):
    file_to_write.write(f"dn: uid={login},ou=People,dc=localdomain\n")
    file_to_write.write(f"objectClass: top\n")
    file_to_write.write(f"objectClass: inetorgperson\n")
    file_to_write.write(f"objectClass: posixAccount\n")
    file_to_write.write(f"cn: {firstname} {name}\n")
    file_to_write.write(f"sn: {name}\n")
    file_to_write.write(f"givenname: {firstname}\n")
    file_to_write.write(f"userPassword: {password}\n")
    file_to_write.write(f"gidNumber: 100\n")
    file_to_write.write(f"uidNumber: {uid_number}\n")
    file_to_write.write(f"homeDirectory: /home/{login}\n")
    file_to_write.write(f"loginShell: /bin/bash")


def main():
    file = "liste-login-pass.csv"
    counter = 0

    uid_is_set = False

    with open(file, newline='') as list:
        student_list = csv.reader(list, delimiter=";")

        for line in student_list:
            name = line[0]
            firstname = line[1]
            current_year = line[2][0]
            student_id = line[3]
            password = line[4]

            if uid_is_set is False:
                uid_number = str(sys.argv[1])
                uid_is_set = True
            else:
                uid_number = str(int(uid_number) + 1)

            with open("create_global_user.ldif", "w") as global_students:
                create_global_user(name, firstname, uid_number, student_id, password, global_students)

            os.popen("ldapadd -D 'cn=Directory Manager' -f /root/Documents/2_scripts/create_global_user.ldif -x -W").read()

            if current_year == "1":
                os.popen(f"setquota -u {student_id} 150000 150000 0 0 /home").read()
            else:
                os.popen(f"setquota -u {student_id} 200000 200000 0 0 /home").read()

            if counter == 3:
                break
            else:
                counter += 1


if __name__ == '__main__':
    main()
