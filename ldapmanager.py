#!python3.6

import os

menu_options = {
    1: 'Group1',
    2: 'Group2',
    3: 'Back',
}
main_options = {
    1: 'Create User',
    2: 'Delete User',
    3: 'Change password',
    4: 'Exit',
}


def print_main():
    for key in main_options.keys():
        print(key, '--', main_options[key])


def print_menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def main_menu():
    print_main()
    option = ''
    try:
        option = int(input('Enter your choice: '))
    except:
        print: ('Wrong input. Please enter a number...')
    if option == 1:
        create_user()
    if option == 2:
        delete_user()
    if option == 3:
        chng_pswd()
    if option == 4:
        print('exiting')
    exit()


def gid_menu():
    print_menu()
    option = ''
    try:
        option = int(input('Enter your choice: '))
    except:
        print: ('Wrong input. Please enter a number... ')
    if option == 1:
        return 2000
    if option == 2:
        return 3000
    if option == 3:
        main_menu()


def finduid(gid):
    clidata = os.popen(
        "ldapsearch -x -b 'dc=dezmeana,dc=local,dc=au' | grep -B 1 %s | grep uid" % gid).read()
    data = [int(i) for i in clidata.split() if i.isdigit()]
    newuid = (max(data))
    intrimuid = newuid + + 1
    if intrimuid in data:
        uid = intrimuid + + 1
        return uid
    else:
        return intrimuid


def create_user():
    usr = input("Enter username: ")
    fname = input("Enter firstname: ")
    lname = input("Enter lastname: ")
    gid = gid_menu()
    uid = finduid(gid)
    # adding user varibles to the ldap user form.
    ldap = open("ldap.txt", 'r')
    data = ldap.read()
    data = data.replace('{usr}', str(usr))
    data = data.replace('{lname}', str(lname))
    data = data.replace('{fname}', str(fname))
    data = data.replace('{gid}', str(gid))
    data = data.replace('{uid}', str(uid))
    ldap.close()

    # writing data to the ldif in the correct folder.
    ldap_form = open("/root/%s.ldif" % usr, "wt")
    ldap_form.write(data)
    ldap.close()

    # display data written to be visually checked before proceeding.
    print(data)

    # Binding new accout to ldap.
    os.system('sudo ldapadd -x -W -D "cn=admin,dc=dezmeana,dc=local,dc=au" -f /root/%s.ldif' % usr)
    os.system('sudo ldappasswd -S -W -D "cn=admin,dc=dezmeana,dc=local,dc=au" -x "uid=%s,ou=people,dc=dezmeana,dc=local,dc=au"' % usr)
    main_menu()


def delete_user():
    main_menu()


def chng_pswd():
    usr = input("Enter username: ")
    os.system('ldappasswd -S -W -D "cn=admin,dc=dezmeana,dc=local,dc=au" -x "uid=%s,ou=people,dc=dezmeana,dc=local,dc=au"' % usr)
    main_menu()


if __name__ == '__main__':
main_menu()
