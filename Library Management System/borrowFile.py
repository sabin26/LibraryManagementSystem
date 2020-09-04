from datetime import datetime
import string
import read_display as rd


'''Asking the user to provide the details of the borrower and book names they want to borrow
   Restricting the user to lend atmost 2books to each student'''
def borrow_book():
    global inputBooks_list
    global student_name
    rd.read_file()
    print('\n'+(' '*55)+'If multiple books are to be borrowed then write their names separated with commas')
    print('\n'+(' '*50)+'Lending duration for borrowed book/s is 10 days. If late to return then fine is $2 per day')
    special_char = set(string.punctuation)
    while True:
        student_name = input('\nName of the borrower: ')
        if student_name.isspace() or student_name.isdigit() or any(char in special_char for char in student_name):
            print('\nInvalid Input')
            continue
        else:
            break
    while True:
        book_name = input('\nBorrowing Books: ')
        if len(book_name.split(',')) >= 3 :
            print('\nA student is only allowed to borrow atmost 2 books')
            continue
        else:
            break
    inputBooks_list = []
    for book in book_name.split(','):
        book_withoutSpace = book.rstrip().lstrip()
        inputBooks_list.append(book_withoutSpace.lower())
    check_books()                    

'''Checking if the books requested to be borrowed is/are avaiable or not
   If available then only the books can be borrowed'''
def check_books():
    global common_books
    global uncommon_books
    rd.read_file()
    list_of_books = []
    userInput_books = set(inputBooks_list)
    for index in range(1, len(rd.book_details)):
        each_book = rd.book_details[index][0]
        list_of_books.append(each_book.lower())
    books_in_library = set(list_of_books)
    common_books = list(userInput_books.intersection(books_in_library))
    uncommon_books = list(userInput_books.difference(books_in_library))
    borrowing_process()    

'''This function checks if the book is out of stock or available in limited value
and also updates the stock of the books if it is borrowed'''
def borrowing_process():
    global counter
    counter = 0
    if common_books == []:
        print('\nThe book/s entered is unavailable in our library')
    else:
        global listOfBorrowedBooks
        global amount
        if uncommon_books != []:
            print('\nThe following books are unavailable:')
            for book in uncommon_books:
                print('\n'+book)
        amount, counter = 0, 0
        listOfBorrowedBooks = []
        del(rd.book_details[0])
        for book in common_books:
            input2 = True
            while input2 == True:
                while True:
                    try:
                        book_quantity = int(input('\nQuantity of books for '+book+':' ))
                        if book_quantity == 0:
                            print('\nInvalid Input')
                            continue
                        elif book_quantity > 2 and len(common_books) == 1:
                            print('\nA student is only allowed to borrow atmost 2 books')
                            continue
                        elif book_quantity > 1 and len(common_books) == 2:
                            print('\nWhen borrowing multiple books, a student is only allowed to borrow one piece of each book')
                            continue
                        else:
                            break       
                    except:
                        print('\nInvalid Input')
                        continue
                for k in range(len(rd.book_details)):
                    eachBook = rd.book_details[k][0]
                    if book == eachBook.lower() and book_quantity <= int(rd.book_details[k][2]) and int(rd.book_details[k][2]) != 0:
                        price = float(rd.book_details[k][3].replace('$', ''))
                        amount = amount + (book_quantity*price)
                        rd.book_details[k][2] = str(int(rd.book_details[k][2]) - book_quantity)
                        counter = 1
                        file2 = open('books.txt', 'w')
                        for i in range(len(rd.book_details)):
                            updatedData = ', '.join(rd.book_details[i])
                            file2.write(updatedData+'\n')
                        file2.close()
                        input2 = False
                        listOfBorrowedBooks.append(eachBook)
                        break
                    elif book == eachBook.lower() and book_quantity > int(rd.book_details[k][2]) and int(rd.book_details[k][2]) != 0:
                        print('\n'+eachBook+' is limited in stock')
                        break
                    elif book == eachBook.lower() and int(rd.book_details[k][2]) == 0:
                        print('\n'+eachBook+' is out of stock')
                        input2 = False
                        break
                    else:
                        pass
    borrow_note()

'''It makes record of the books borrowed and appends to a single file
   It also creates new files for each student and stores the record of books borrowed'''             
def borrow_note():
    if counter == 1:
        listing = [student_name.title(), (' - '.join(listOfBorrowedBooks)).title(), '$'+str(amount), datetime.now().strftime('%Y-%m-%d %I:%M %p')]
        details = ['Name of the borrower: ', '\nBorrowed Book/s: ', '\nTotal amount to be paid: ', '\nIssued Date/Time: ']
        file3 = open('borrowed_note.txt', 'a+')
        file7 = open('allBorrowedAndReturnedNotes/borrowedBy'+student_name.title()+'.txt', 'a+')
        print('\n'+'.'*35)
        file7.write('\n'+'.'*67)
        file3.write('\n'+'.'*67)
        for value in range(len(details)):
            print(details[value]+listing[value])
            file3.write('\n'+details[value]+listing[value])
            file7.write('\n'+details[value]+listing[value])
        print('.'*35)
        file3.write('\n'+'.'*67)
        file7.write('\n'+'.'*67)
        file3.close()
        file7.close()
    backToMain()

# This function takes user back to the library menu
def backToMain():
    import mainProgram as m
    m.choose_options()
