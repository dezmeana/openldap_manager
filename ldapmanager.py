#!python3.6

import os

# menu to identify the GID
menu_options = {
    1: 'Group1',
    2: 'Group2',
    3: 'Back',
}
# first menu you see when running the script.
main_options = {
    1: 'Create User',
    2: 'Delete User',
    3: 'Change password',
    4: 'Exit',
}


# wonder if I can merge the next two into one since they the same function
def print_main():
    for key in main_options.keys():
        print(key, '--', main_options[key])


# as baove
def print_menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


# main menu options and triggers
def main_menu():
    print_main()
    option = ''
    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number...')
    if option == 1:
        create_user()
    if option == 2:
        delete_user()
    if option == 3:
        chng_pswd()
    if option == 4:
        print('exiting')
    exit()


# menu option to identify GID
def gid_menu():
    print_menu()
    option = ''
    try:
        option = int(input('Enter your choice: '))
    except:
        print('Wrong input. Please enter a number... ')
    if option == 1:
        return 2000
    if option == 2:
        return 3000
    if option == 3:
        main_menu()


# Use the GID defined to find the next available
# GID in a list return from open ldap
def finduid(gid):
    clidata = os.popen("ldapsearch -x -b 'dc=dezmeana,dc=local,dc=au'\
     | grep -B 1 %s | grep uid" % gid).read()
    data = [int(i) for i in clidata.split() if i.isdigit()]
    newuid = (max(data))
    intrimuid = newuid + + 1
    if intrimuid in data:
        uid = intrimuid + + 1
        return uid
    else:
        return intrimuid


# takes users inputs and defined GID and UID to create a new user in openldap
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
    os.system('ldapadd -x -W -D "cn=admin,dc=dezmeana,dc=local,dc=au" \
    -f /root/%s.ldif' % usr)
    os.system('ldappasswd -S -W -D "cn=admin,dc=dezmeana,dc=local,dc=au" \
    -x "uid=%s,ou=people,dc=dezmeana,dc=local,dc=au"' % usr)
    main_menu()


# TODO complete the delete user module
def delete_user():
    main_menu()


# function to delete user
def chng_pswd():
    usr = input("Enter username: ")
    os.system('ldappasswd -S -W -D "cn=admin,dc=dezmeana,dc=local,dc=au" \
    -x "uid=%s,ou=people,dc=dezmeana,dc=local,dc=au"' % usr)
    main_menu()


if __name__ == '__main__':
    main_menu()
