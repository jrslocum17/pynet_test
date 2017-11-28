#!/usr/bin/env python

from mytest import *
# could also use "from mytest import func1, func2, func3, MyClass"

def main():
    print("Now calling func1")
    func1()
    print("Now calling func2")
    func2()
    print("Now calling func3")
    func3()

    myObj = MyClass("upper", "mid", "lower")
    print("now calling hello method")
    myObj.hello()
    print("now calling not_hello method")
    myObj.not_hello()


if __name__ == "__main__":
    main()
