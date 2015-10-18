#!/usr/bin/python

import sys,glob

def u2d(s,d,fmt): # s and d can be the same
  # open, read, close s
  print( fmt%s, end="" )
  o = b""
  k = False
  f = open(s,"rb")
  for t in f:
    ##u = t.replace(b"</td>",b"</td>\n").replace(b"</tr>",b"</tr>\n").replace(b"<br>",b"<br>\n")
    u = t.replace(b"\n",b"\r\n").replace(b"\r\r",b"\r")
    if u != t: k = True
    o += u
  f.close()
  print( "R", end="" )
  if k:
    # create, write, close d
    f = open(d,"wb")
    f.write( o )
    f.close()
    print( "W" )
  else:
    print( "+" )

if len(sys.argv)==1:
  print( "Converts in each argument file <NL> into <CR><NL>" )
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
  fmt = "%%-%ds "%mxl
  for n in lst:
    u2d(n,n,fmt)
