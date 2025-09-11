class Student:
    def __init__(self,name,rollno,marks):
        self.name=name
        self.rollno=rollno
        self.marks=marks
    def display(self):
        print('Name of the student is:'+self.name)
        print('Roll of the student is:'+str(self.rollno))
        print('Marks of the student is:'+str(self.marks))
s1=Student("rishitha",6732,98)
s2=Student("rishi",5,77)
s1.display()
s2.display()