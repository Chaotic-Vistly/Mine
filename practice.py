system = 0
while system == 0:
    username = str(input('Please Enter your username: '))
    usernames = list(("Viktor", 'Ivan', 'Zack', 'Aizen'))
    if username in usernames:
        print('That username already exists!')
    else:
        usernames.append(username)
        password = input("Please enter your password: ")
        print(f" Your username is {username}")
        a = input('Do you want to see you password? ').lower()
        if a == "yes":
            print(f'Your password is {password}')
            system = 1
        else:
            system = 1
        while system == 1:
            check1 = input('Please enter your username: ')
            check2 = input('Please enter your password: ')
            if check1 == username and check2 == password:
                print(f'\nCongratulation you are logged in. Welcome {username}!')
                system = 7
                print(usernames)
            else:
                print('Incorrect username and password.')

