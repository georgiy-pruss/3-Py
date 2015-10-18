#!/usr/bin/python

import os,os.path,sys,glob
from stat import *

def calcsz(f):
  st = os.stat(f)
  md = st[ST_MODE]
  if S_ISLNK(md):
    return 0
  if S_ISDIR(md):
    ss = 0
    try:
      for x in os.listdir(f):
        ss += calcsz(os.path.join(f,x))
    except WindowsError as e:
      return -1
    return ss
  if S_ISREG(md):
    return st.st_size
  print('?',f,md)
  return 0

def doargs(dd):
  ss = 0
  for d in dd:
    if '*' in d or '?' in d:
      s1 = doargs(glob.glob(d))
    else:
      s1 = calcsz(d)
    print("%11d"%s1,d)
    ss += s1
  return ss

print("\n%11d *"%doargs(sys.argv[1:]))

