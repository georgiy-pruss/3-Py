# Usage: svn st | svncolor.py  or  svn diff ... | svncolor.py

import sys
from utils import sc,wr,p

short_colors = { 'M':"R", '?':"M", 'A':"G", 'X':"Y", 'C':"kR", '-':"R", 'D':"rW",  '+':"G" }
long_colors = { "Property changes":"-", "____":"-", # skip line
  "---":"R", "+++":"G", "@@":"C", "====":"W", "Index: ":"Y" }

def colorize(line):
  done = False
  for c in long_colors:
    if line.startswith(c):
      if long_colors[c]=="-":
        return
      else:
        sc(long_colors[c]); done = True; break
  if not done:
    for c in short_colors:
      if line.startswith(c):
        sc(short_colors[c]); break
  p(line); sc(); p()

if __name__ == '__main__':
  for line in sys.stdin:
    colorize( line.rstrip() )
