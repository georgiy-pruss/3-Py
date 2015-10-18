####!/bin/usr/python3

import sys
if len(sys.argv)<5:
  print( "convert_unicode.py src_utf8.htm dst_cp1251.htm UTF8 CP1251" )
  print( "                 | src_cp1251.htm dst_koi8r.htm cp1251 koi8-r" )
  print( "                 | src_utf8.htm dst_utf16le.htm utf8 utf-16-le 16le" )
  print( "last extra arg is bom: 8 or 16le or 16be" )
  print( "See http://docs.python.org/py3k/library/codecs.html#standard-encodings\n"+
    "for encoding list (or c:/bin/standard-encodings.htm)" )
  sys.exit(0)
fi,fo,ci,co = sys.argv[1:5]
bom = len(sys.argv)==6 and sys.argv[5] or ""
bbom = {"":b"","8":b"\xEF\xBB\xBF","16le":b"\xFF\xFE","16be":b"\xFE\xFF"}[bom]
#open(fo,"wb").write( open(fi,"rb").read().decode(ci,'ignore').encode(co,'ignore') )
input = open(fi,"rb").read()
output = input.decode(ci,'backslashreplace').encode(co,'backslashreplace')
h = open(fo,"wb")
h.write( bbom + output )
h.close()
