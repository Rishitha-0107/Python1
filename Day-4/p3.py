from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
class Rectangle(Shape):
    def __init__(self, length, breadth):
        self.length = length      
        self.breadth = breadth
    def area(self):
        print("Area of rectangle is:", self.length * self.breadth)
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius      

    def area(self):
        print("Area of circle is:", 3.14 * self.radius * self.radius)
r = Rectangle(6, 3)
c = Circle(5)
r.area()
c.area()
