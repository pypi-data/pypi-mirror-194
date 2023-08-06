from sys import *
from time import *

def write_string(string):
    for letter in string:
        stdout.write(letter)
        stdout.flush()
        sleep(0.05)
    print("")

def slow_write(string):
    for letter in string:
        stdout.write(letter)
        stdout.flush()
        sleep(1)
    print("")

def medium_write(string):
    for letter in string:
        stdout.write(letter)
        stdout.flush()
        sleep(0.5)
    print("")

def fast_write(string):
    for letter in string:
        stdout.write(letter)
        stdout.flush()
        sleep(0.005)
    print("")
