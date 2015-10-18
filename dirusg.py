#!/usr/bin/python

import os,os.path,sys,utils
from stat import *

args = sys.argv[1:]
if not args or args==["-n"]:
  print "Syntax: dirusg.py [-n] dirs/files -- to calculate their total size [-n to ignore dirs]"
  sys.exit(0)
NODIRS=False
if args[0]=="-n":
  NODIRS=True
  args = args[1:]

def calcsz(f):
  """Return size of dir, or negative size of file, or 0 in other cases"""
  if f in (".",".."):
    return 0
  if os.path.islink(f):
    return 0
  try: 
    st = os.stat(f)
  except OSError,e:
    print "?S",str(e)
    return 0
  md = st[ST_MODE]
  if S_ISLNK(md) or os.path.islink(f):
    return 0
  if S_ISDIR(md):
    if NODIRS: return 0
    ss = 0
    try:
      for x in os.listdir(f):
        pathname = os.path.join(f,x)
        ss += abs(calcsz(pathname))
    except OSError,e:
      print "?D",str(e)
    return ss
  if S_ISREG(md):
    return -st.st_size
  return 0

ss = 0
sf = 0 # size of files
nf = 0 # number of files
tf = '' # if one file, its name
for d in args:
  if d in (".",".."): continue
  s1 = calcsz(d)
  if s1 < 0: # simple file
    nf += 1
    sf += -s1
    ss += -s1
    tf = d         
  elif not NODIRS:
    print "%13s"%utils.format_int(s1),d
    ss += s1
if nf>1:
  print "\n%13s [%d files]"%(utils.format_int(sf),nf)
elif nf>0:
  print "\n%13s %s"%(utils.format_int(sf),tf)
print "\n%13s *****"%utils.format_int(ss)
