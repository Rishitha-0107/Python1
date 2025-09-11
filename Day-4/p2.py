class Employee:
    def __init__(self,name,salary):
        self.name=name
        self.salary=salary
    def display(self):
        print("Name: " + self.name + "Salary: " + self.salary)
class Manager(Employee):
    def __init__(self,department):
        self.department=department
    def display(self):
        print("Department: "+self.department)
e=Employee("Rishitha","90000")
m=Manager("IT")
e.display()
m.display()
