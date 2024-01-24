import random
import os


def create_group(groupname, gid_number):
    return os.popen(f'samba-tool group add {groupname} --gid-number {gid_number} --nis-domain SUPERCOMPTA').read()


def create_user(name, firstname, username, password, gid_number):
    return os.popen(
        f'samba-tool user create {username} {password} --use-username-as-cn --given-name={firstname} --surname={name} --gid-number {gid_number} --login-shell=/bin/bash --unix-home=/home/{username} --profile-path="C:\\UserData\{username}\profile" --home-directory="C:\\Users\{username}"').read()


def add_user_to_group(username, group):
    return os.popen(f'samba-tool group addmembers {group} {username}')


def generate_password():
    password = os.popen('mkpasswd -l 12 -c 4 -C 4 -d 4 -s 0').read()
    return password


def add_users_to_ad(source_file, group):
    with open(source_file, 'r') as list:
        user_list = list.readlines()
        users_to_file = []

        if group is "Management":
            users = random.choices(user_list, k=1)
            gid_number = 5000
        elif group is "Techniciens":
            users = random.choices(user_list, k=2)
            gid_number = 5001
        elif group is "RH":
            users = random.choices(user_list, k=2)
            gid_number = 5002
        elif group is "Comptables":
            users = random.choices(user_list, k=15)
            gid_number = 5003

        for line in users:
            user = line.rstrip()
            firstname, name = user.split(sep=".")
            username = (firstname + name).lower()
            # password = generate_password()
            password = "P@ssw0rd"

            user = f"{firstname};{name};{username};{password};{group};{gid_number}"
            users_to_file.append(user)
            create_user(name, firstname, username, password, gid_number)
            add_user_to_group(username, group)

        return users_to_file


def main():
    file = "list-of-users.csv"
    groups = {"Management": 5000,
              "Techniciens": 5001,
              "RH": 5002,
              "Comptables": 5003}

    for group, gid_number in groups.items():
        create_group(group, gid_number)
        users_to_file = add_users_to_ad(file, group)
        for user in users_to_file:
            os.popen(
                f"echo '{user}' >> ./AD-users.csv")


if __name__ == '__main__':
    main()
