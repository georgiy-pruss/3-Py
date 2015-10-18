#!/usr/bin/python
#$HOME/Py/utils.py
#set PYTHONPATH="$HOME/Py"

__doc__="""
set_pos( row=0, col=0 ) | ( -1 | -2 ) -- neg. for save/restore
sc( fg="C", bg="k" ) -- set color; from kbgcrmywKBGCRMYW
wr( x ) -- sys.stdout.write( x )
p( *x ) -- wr all x; p() -- NEWLINE
format_int( n, sep=",", grp=3 )
wrap_lines( array_of_words, max_width, sep=NEWLINE )
join( array, sep=" " )
amend( s, n, remove=1, insert="" )
log( file_name, msg )
"""

import sys

# Console Colors.

_SYSCOLORS = "krgybmcwKRGYBMCW"

def sc( fg="w", bg="k" ):
  """Set color""" # TODO: # 3 it(no) 4 und 5 bln 7 neg
  if len(fg)==2:
    bg=fg[1:]; fg=fg[:1]
  f = _SYSCOLORS.index(fg)
  if f<0: f=7
  b = _SYSCOLORS.index(bg)
  if b<0: b=0
  sys.stdout.write("\033[%dm\033[%dm\033[%dm"%(f>>3,30+f%8,40+b%8))

# reset color
import atexit
atexit.register(sc)

def wr(x,file=sys.stdout):
  """Write to stdout or other file/stream"""
  file.write(x)

def p(*x):
  """Print to stdout"""
  file=sys.stdout
  if len(x)==0:
    file.write("\n")
    return
  for e in x:
    file.write(str(e))
  file.flush()

def set_pos( row=0, col=0 ):
  """Example: set_pos(), set_pos(10), set_pos(2,40);
  Special: set_pos(-1) - save; set_pos(-2) - restore
  """
  if row < 0:
    wr( row==-1 and "\033[s" or "\033[u" )
  else:
    wr("\033[%d;%df"%(row+1,col+1)) # f or H

# Misc fns

def format_int(n,sep=',',grp=3):
  if n<0: return "-"+format_int(-n)
  g = -grp
  s = str(n)
  r = s[g:]
  s = s[:g]
  while len(s)>0:
    r = s[g:] + sep + r
    s = s[:g]
  return r

def wrap_lines( arr_words, max_width, sep='\n' ):
  line = arr_words[0]
  llen = len(line)
  for word in arr_words[1:]:
    wlen = len(word)
    if llen+1+wlen > max_width:
      line += sep; llen = 0
    else:
      line += ' '; llen += 1
    line += word
    llen += wlen
  return line

def join( arr, sep=' ' ):
  return sep.join( arr )

def amend( s, n, remove=1, insert="" ):
  "remove some letters and replace them with another string"
  return s[:n]+insert+s[n+remove:]

def log( file_name, msg ):
  log_file = file( file_name, 'at' )
  dt = '%04d-%02d-%02d %02d:%02d:%02d' % time.localtime()[:6]
  print >>log_file, dt, msg
  log_file.close()


if __name__=="__main__":
  p(sys.version)
  for b in _SYSCOLORS:
    p()
    for f in _SYSCOLORS:
      sc( f, b ); p( "%c/%c "%(f,b) )
    sc()

# EOF
