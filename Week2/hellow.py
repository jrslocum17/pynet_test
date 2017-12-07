#!/usr/bin/env python
"""
This program prints out Hello World

 Ex 1c. Write a simple Python module that contains one function that prints 'hello' (module name = my_func.py).
 Do a test where you import my_func into a new Python script. Test this using the following contexts:
        * my_func.py is located in the same directory as your script
        * my_func.py is located in some random subdirectory (not the same directory as your script)
        * my_func.py is located in ~/applied_python/lib/python2.7/site-packages/

"""

import my_func
def main():
    my_func.HelloWorld()

if __name__ == "__main__":
    main()
