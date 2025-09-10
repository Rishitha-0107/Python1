#program for implemntation of library managment system in python dictionaries
def libsys():
    library={}
    while True:
        print("\nLibrary Management System")
        print("1.Add a book")
        print("2.Remove a book by ID")
        print("3.Search for a book by ID")
        print("4.Update book title by ID")
        print("5.Display all books")
        print("6.Count total books")
        print("7.Check if a title exists")
        print("8.Exit")
        ch=input("Enter your choice: ")
        if ch=='1':
            id=input("Enter Book ID: ")
            if id in library:
                print("Book ID already exists")
            else:
                t=input("Enter Book Title:")
                library[id]=t
                print("Book is added")
        elif ch=='2':
            id=input("Enter Book ID to remove: ")
            rt=library.pop(id, None)  
            if rt:
                print("Book with that id is removed")
            else:
                print("Book ID not found")
        elif ch=='3':
            id=input("Enter Book ID to search: ")
            t=library.get(id) 
            if t:
                print(f"Book found: '{title}'")
            else:
                print("Book ID not found")
        elif ch=='4':
            id=input("Enter Book ID to update: ")
            if id in library:
                nt= input("Enter new title: ")
                library.update({id:nt})  
                print(f"Book ID {id} updated to '{nt}'")
            else:
                print("Book ID not found")
        elif ch=='5':
            if library:
                print("\nAll books in the library:")
                for id, title in library.items(): 
                    print(f"ID:{id},Title:{title}")
            else:
                print("Library is empty")
        elif ch=='6':
            print("Total number of books:",len(library))  
        elif ch=='7':
            tc=input("Enter book title to check: ")
            if tc in library.values(): 
                print(f"Book title '{tc}' exists in the library")
            else:
                print(f"Book title '{tc}' does not exist")
        elif ch=='8':
            print("Exiting Library Management System")
            break
        else:
            print("Invalid choice")
libsys()
