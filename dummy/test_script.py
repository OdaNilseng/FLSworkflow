import math


class Test(object):
    def __init__(self, length):
        self.length = length
        area = self.area()

    def area(self):
        a = self.length**2
        print(a)
        return a

    def circumference(self):
        return self.length * 4

"""
def area(length):
    print(length * length)

def circumference(length):
    return length * 4
"""