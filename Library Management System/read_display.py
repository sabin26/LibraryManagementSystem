
''' Reading the book details from a text file and
storing the information on a 2d list '''
def read_file():
    global book_details
    book_details = [['Book Name', 'Author', 'Stock', 'Price(per book)']]
    file = open('books.txt', 'r')
    for line in file.readlines():
        list = []
        for each in line.split(', '):
            list.append(each.replace('\n', ''))
        book_details.append(list)
    file.close()
    
# Displaying the available books in a library
def available_books():
    read_file()
    print('.'*142)
    for items in range(len(book_details)):
        for item in book_details[items]:
            print(item, end=(' '*(42-len(item))))
        if items != (len(book_details)-1):
            print('\n')
        else:
            print()
    print('.'*142)
    backToMain()

# This function takes user back to the Library menu
def backToMain():
    import mainProgram as p
    p.choose_options()
