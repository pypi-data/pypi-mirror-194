#!/usr/bin/env python
"""
move unfinished tasks back to heap
"""
import os, sys, glob, yaml, subprocess
from yui import tsklib

def main():
    argv = sys.argv;
    argv.pop(0); # remove first element, pointing to script itself
    if len(argv) != 1 :
        print("""
        Usage:
            """+tsklib.cmd+""" reset %taskId%   - move single task back to heap by id
            """+tsklib.cmd+""" reset id%taskId%   - move single task back to heap by id
            """+tsklib.cmd+""" reset cur%taskNum%   - move single task back to heap, using order number from """+tsklib.cmd+""" list cur
            """+tsklib.cmd+""" reset all        - move all unfinished tasks back to heap
        Example:
            """+tsklib.cmd+""" pick 3
            """+tsklib.cmd+""" pick id3
            """+tsklib.cmd+""" pick cur3
            """)
        exit(1);
        pass;
    id = argv[0]
    tasks = []

    if id == "all":
        tsklib.resetAll()
        return
        pass
    
    tsklib.resetTask( id )
    
    pass

if __name__=="__main__":
    main()
    pass


