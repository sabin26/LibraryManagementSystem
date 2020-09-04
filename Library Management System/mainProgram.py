import read_display as rd
import borrowFile as b
import returnFile as r

# Greeting the user to the library Management System   
def greeting():
    print('\n'+(' '*75)+'Welcome to the Library Management System\n')

''' Creating a Library menu where different options are provided
    like fetching books information, borrowing/returning books and closing the program'''
def choose_options():
    print('\n'+('-'*15)+'Library Menu:'+('-'*15))
    options = ['Get books info', 'Borrow book/s', 'Return book/s', 'Exit']
    for option in range(len(options)):
        print((' '*32)+str(option+1)+')'+options[option]+'\n')
    user_choice()

''' Asking the user to select an option
    If 1 is pressed, books details are displayed
    If 2 is pressed, books can be borrowed
    If 3 is pressed, books can be returned
    If 4 is pressed, program terminates'''    
def user_choice():
    while True:
        while True:
            try:
                selected_one = int(input('\nChoose an option: '))
                break
            except:
                print('\nInvalid Input')
                continue
        if selected_one == 1:
            rd.available_books()
            break
        elif selected_one == 2:
            b.borrow_book()
            break
        elif selected_one == 3:
            r.returnBook()
            break
        elif selected_one == 4:
            exit()
        else:
            print('\nInvalid Input')

# If program is running from main file then only the given functions are called
if __name__ == "__main__":
    greeting()
    choose_options()
