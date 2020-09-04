from datetime import datetime
import string
import read_display as rd

''' Asks the user for book names to be returned and their quantity
    Checks if the books returned were actually borrowed from the library or not '''
def returnBook():
    global inputBook_list
    global booksQuantity
    global nameOfTheBorrower
    var = 0
    rd.read_file()
    booklist = []
    for index in range(1, len(rd.book_details)):
        each_book = rd.book_details[index][0]
        booklist.append(each_book.lower())
    print('\n'+(' '*55)+'If multiple books are to be returned then write their names separated with commas')
    specialChars = set(string.punctuation)
    while True:
        nameOfTheBorrower = input('\nName of the borrower: ')
        if any(char in specialChars for char in nameOfTheBorrower) or nameOfTheBorrower.isdigit() or nameOfTheBorrower.isspace():
            print('\nInvalid Input')
            continue
        else:
            break
    readBorrowedNote()
    for loop in dictionary.keys():
        if loop == nameOfTheBorrower.title():
            print('\nThe following books are borrowed by '+nameOfTheBorrower.title()+': '+dictionary[loop][0])
            while True:
                returningBook = input('\nReturning book/s: ')
                inputBook_list = []
                booksQuantity = {}
                for book in returningBook.split(','):
                    book_withoutSpace = book.rstrip().lstrip()
                    if book_withoutSpace.lower() not in booklist:
                        print('\n'+book_withoutSpace.title()+' is not from our library')
                        answer = input('\nRe-enter all book names ? (yes/no) ')
                        if answer.lower() == 'yes':
                            var = 2
                            break
                    elif book_withoutSpace.lower() in booklist and book_withoutSpace.lower() not in dictionary[loop][0].lower().split(' - '):
                        print('\nThe person has not borrowed the book '+book_withoutSpace.title())
                        print('Please re-enter the books name again')
                        var = 2
                        break
                    elif book_withoutSpace.lower() in booklist and book_withoutSpace.lower() in dictionary[loop][0].lower().split(' - '):
                        inputBook_list.append(book_withoutSpace.lower())
                        while True:
                            try:
                                bookQuantity = int(input('\nQuantity of books for '+book_withoutSpace.title()+': '))
                                if bookQuantity != 0:
                                    break
                                else:
                                    print('\nInvalid Input')
                                    continue
                            except:
                                print('Invalid Input')
                                continue
                        booksQuantity[book_withoutSpace.title()] = bookQuantity
                        var = 1
                if var != 2:
                    break  
            break
    if var == 0:
        print('\nThe person has not borrowed any book')
        backToMain()
    else:
        returningProcess()

'''Reading the note where the record of borrowed books are stored and
   appending the data into a dictionary'''
def readBorrowedNote():
    global dictionary
    file4 = open('borrowed_note.txt','r')
    lines = file4.readlines()
    l = []
    l2 = []
    e = 0
    for line in lines:
        if e == 9:
            l.append(l2)
            l2 = []
            e = 0
        if e == 8 and line == '.'*67:
            l.append(l2)
        for k in line.split(': '):
            b = k.replace('.'*67, '')
            c = b.replace('\n','')
            if c == 'Name of the borrower' or c == 'Borrowed Book/s' or c == 'Total amount to be paid' or c == 'Issued Date/Time' or c == '':
                pass
            else:
                l2.append(c)
        e = e + 1
    dictionary = {}
    for i in range(len(l)):
        dictionary[l[i][0]] = l[i][1:4]
    file4.close()

'''Returning date is set to system current date and the borrowed date is checked
   If the duration between borrowing and returning date is more than 10 days then fine is generated'''
def returningProcess():
    global fine
    readBorrowedNote()
    initialDate = dictionary[nameOfTheBorrower.title()][2]
    borrowedDate = datetime.strptime(initialDate, '%Y-%m-%d %I:%M %p')
    returnDate = datetime.now()
    dateDifference = returnDate - borrowedDate
    if int(dateDifference.days) > 9 :
        fine = 2*((int(dateDifference.days)+1)-10)
    else:
        fine = 0
    returnedNote()

''' The record of returned books is appended to a file with their respective borrower name
    A single file for each record is generated having the borrower name as the file name'''
def returnedNote():
    title = ['Name of the borrower: ','\nBooks returned: ','\nDate/Time of return: ']
    userInfo = [nameOfTheBorrower.title(), (' - '.join(inputBook_list)).title(), datetime.now().strftime('%Y-%m-%d %I:%M %p')]
    file5 = open('returned_note.txt', 'a+')
    print('\n'+'.'*35)
    file8 = open('allBorrowedAndReturnedNotes/returnedBy'+nameOfTheBorrower.title()+'.txt', 'a+')
    file5.write('\n'+'.'*67)
    file8.write('\n'+'.'*67)
    for value in range(len(userInfo)):
        print(title[value]+userInfo[value])
        file5.write('\n'+title[value]+userInfo[value])
        file8.write('\n'+title[value]+userInfo[value])
    if fine != 0:
        print('\nFine: '+'$'+str(fine))
        file5.write('\n\nFine: '+'$'+str(fine))
        file8.write('\n\nFine: '+'$'+str(fine))
    print('.'*35)
    file5.write('\n'+'.'*67)
    file8.write('\n'+'.'*67)
    file5.close()
    file8.close()
    updatedStock()
    backToMain()

'''The quantity of particular book is updated when a student returns the book
   Then the updated data is written into the file in which the book details are stored'''
def updatedStock():
    rd.read_file()
    del(rd.book_details[0])
    for book in inputBook_list:
        for i in range(len(rd.book_details)):
            if rd.book_details[i][0].lower() == book.lower():
                rd.book_details[i][2] = str(int(rd.book_details[i][2]) + booksQuantity[book.title()])
    file6 = open('books.txt', 'w')
    for i in range(len(rd.book_details)):
        updatedData = ', '.join(rd.book_details[i])
        file6.write(updatedData+'\n')
    file6.close()    

# This function takes user back to the library menu
def backToMain():
    import mainProgram as m
    m.choose_options()
