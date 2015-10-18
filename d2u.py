#!/usr/bin/python

import sys,glob

def d2u(s,fmt):
  print( fmt%s, end="" )
  # open, read, close s
  o = b""
  k = False
  f = open(s,"rb")
  for t in f:
    if b"\r\n" in t:
      k = True
      t = t.replace(b"\r\n",b"\n")
      while b"\r\n" in t: t = t.replace(b"\r\n",b"\n")
    o += t
  f.close()
  print( "R", end="" )
  if k:
    # create, write, close d
    f = open(s,"wb")
    f.write( o )
    f.close()
    print( "W" )
  else:
    print( "+" )

if len(sys.argv)==1:
  print( "Converts in each argument file <CR><NL> into <NL>" )
else:
  lst = []
  mxl = 0
  for n in sys.argv[1:]:
    if "*" in n or "?" in n:
      gn = glob.glob(n)
      for nn in gn:
        if nn not in lst: lst.append(nn)
        if len(nn)>mxl: mxl=len(nn)
    else:
      if n not in lst: lst.append(n)
      if len(n)>mxl: mxl=len(n)
  fmt = ("%%-%ds "%mxl)
  for n in lst:
    d2u(n,fmt)
