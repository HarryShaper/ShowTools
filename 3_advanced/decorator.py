"""
content = assignment
course  = Python Advanced
 
date    = 13.02.2025
email   = contact@alexanderrichtertd.com
"""


"""
0. CONNECT the decorator "print_process" with all sleeping functions.
   Print START and END before and after.

   START *******
   main_function
   END *********


1. Print the processing time of all sleeping functions.
END - 00:00:00


2. PRINT the name of the sleeping function in the decorator.
   How can you get the information inside it?

START - long_sleeping

"""


import time


#*********************************************************************
# DECORATOR
def print_process(func):
    def wrapper(*args, **kwargs):
        print(f"START - {func.__name__}")
        start_time = time.time()
        func(*args, **kwargs)                  # main_function
        end_time = time.time()
        print(f"{func.__name__} time was {end_time - start_time}")
    return wrapper


#*********************************************************************
# FUNC
@print_process
def short_sleeping(name):
    time.sleep(.1)
    print(name)

@print_process
def mid_sleeping():
    time.sleep(2)


@print_process
def long_sleeping():
    time.sleep(4)


long_sleeping()