# UTILITIES
# C:\Python\Lib\site-packages\utils.py

__doc__="""
sc = set_color( fg="C", bg="k" ) -- from kbgcrmywKBGCRMYW
wr( x ) -- sys.stdout.write( x )      [file=...]
p( *x ) -- wr all x; p() -- NEWLINE   [file=...]
format_int( n, sep=",", grp=3 )
wrap_lines( array_of_words, max_width, sep=NEWLINE )
join( array, sep=" " )
log( file_name, msg )
"""

# Console Colors.

# See http://msdn2.microsoft.com/en-us/library/ms682073.aspx

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE= -11
STD_ERROR_HANDLE = -12

#~ FOREGROUND_BLUE = 0x01 # text color contains blue.
#~ FOREGROUND_GREEN= 0x02 # text color contains green.
#~ FOREGROUND_RED  = 0x04 # text color contains red.
#~ FOREGROUND_INTENSITY = 0x08 # text color is intensified.
#~ BACKGROUND_BLUE = 0x10 # background color contains blue.
#~ BACKGROUND_GREEN= 0x20 # background color contains green.
#~ BACKGROUND_RED  = 0x40 # background color contains red.
#~ BACKGROUND_INTENSITY = 0x80 # background color is intensified.

import ctypes

_std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_pos( row=0, col=0, handle=_std_out_handle):
    """(...) -> BOOL
    Example: set_pos(), set_pos(10), set_pos(2,40)
    """
    return ctypes.windll.kernel32.SetConsoleCursorPosition(handle, row*65536+col)

def _set_color(color, handle=_std_out_handle):
    """(color) -> BOOL
    Example: set_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
    """
    return ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)

def set_color( fg="W", bg="k" ):
  if len(fg)==2:
    bg=fg[1:]; fg=fg[:1]
  f = "kbgcrmywKBGCRMYW".index(fg)
  if f<0: f=11
  b = "kbgcrmywKBGCRMYW".index(bg)
  if b<0: b=0
  _set_color(f|(b<<4))

sc = set_color

def reset_color():
  import atexit
  atexit.register(set_color)

import sys

def wr(x,file=sys.stdout):
  """Write to stdout or other file/stream"""
  file.write(x)

def p(*x,file=sys.stdout):
  """Print to stdout or other file/stream"""
  if len(x)==0:
    file.write("\n")
    return
  for e in x:
    s=str(e)
    try:
      file.write(s)
    except UnicodeEncodeError:
      for c in s:
        if ord(c)<128:
          file.write(c)
        else:
          file.write('^%04X'%ord(c))
  file.flush()

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
""" or
import locale
locale.setlocale( locale.LC_ALL, 'ru_RU' )
locale.format_string( "%d", <number>, grouping=True )
"""


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

class StrFile:
  def __init__(self,name,mode,encoding=None):
    self.t = False
    self.n = b"\n"
    if 't' in mode:
      self.t,self.n = True,"\n"
    self.f = open(name,mode,encoding=encoding)
  def __lshift__(self,x):
    if not self.t: x = x.encode("utf-8")
    self.f.write( x )
    self.f.write( self.n )
  def close(self):
    self.f.close()

if __name__=="__main__":
  import sys
  p('sys.version: '); p(sys.version)
  for b in "kbgcrmywKBGCRMYW":
    p()
    for f in "kbgcrmywKBGCRMYW":
      sc(f,b);p("%c/%c "%(f,b))
  sc("w","k")

# EOF
