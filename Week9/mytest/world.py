#!/usr/bin/env python


def func1():
    print("this is world func1")


class MyClass(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def hello(self):
        print("My variables forwards are {}, {} and {}".format(self.x, self.y, self.z))

    def not_hello(self):
        print("My variables backwards are {}, {} and {}".format(self.z, self.y, self.x))

class MyChildClass(MyClass):
    def __init__(self, x, y, z):
        self.xy = "{}{}".format(x, y)
        super(MyChildClass, self).__init__(x, y, z)
        # could also do MyClass.__init__(self, x, y, z) but this has differences when it comes to multiple inheritance

    def hello(self):
        print("My variables forwards are {:*<15}  {:*^15}  {:*>15}".format(self.x, self.y, self.z))
        print("My concat variable is {}".format(self.xy))


def main():
    print("this is world main")

if __name__ == "__main__":
    main()

    # some tests
    print("Testing MyClass")
    myObj = MyClass("red", "green", "blue")
    print myObj.x, myObj.y, myObj.z
    myObj.hello()
    myObj.not_hello()
    print
    print("Testing MyChildClass")
    newObj = MyChildClass("up", "down", "left")
    newObj.hello()
    newObj.not_hello()
