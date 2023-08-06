#!/bin/python
import os, sys;
from yui import tsklib

def main():
    archives = tsklib.listArchives()
    counter=0
    for archive in archives:
        print(archive, end="\t")
        counter = counter+1
        if counter == 5:
            print()
            counter=0
            pass
        pass
    print()
    pass

if __name__=="__main__":
    main()
    pass
