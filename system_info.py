#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# python2 usable
import os

def uname_func():
    UNAME="uname -a"
    os.system(UNAME)

def diskspace_func():
    DISKSPACE="df -h"
    os.system(DISKSPACE)

def main():
    uname_func()
    diskspace_func()
if __name__=="__main__":
    main()
