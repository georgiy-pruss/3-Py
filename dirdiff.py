#!/usr/bin/python

import time,sys,shutil,os,os.path
DFLT="+[]c"

if len(sys.argv) < 3:
  print "Syntax: diffdirs.py [opt] dir-1 dir-2 [-x subdir-1 ...]"
  print "opt is sequence of characters:"
  print "  =  show equal files"
  print "  <  show files when left newer"
  print "  >  show files when right newer"
  print "  [  show files unique in left (default)"
  print "  ]  show files unique in right (default)"
  print "  +  show directories i.e. recursive (default)"
  print "  -  do not show conflicts - file and dir with the same name"
  print "  s  compare contents of files with different date and don't show the same"
  print "  h  hide dir. full names"
  print "  c  use colors in output (default)"
  print "default is \"%s\" i.e. show everything" % DFLT
  print "  ~  means different size"
  print "  %  means conflict: file vs dir"
  print "Option -x excludes subdirs from comparison; e.g. adminhelp bin/java ia-jre"
  sys.exit(0)

if len(sys.argv)==3 or len(sys.argv)>3 and sys.argv[3]=="-x":
  opt = DFLT
  src = sys.argv[1]
  dst = sys.argv[2]
  xcl = sys.argv[3:]
else:
  opt = sys.argv[1]
  src = sys.argv[2]
  dst = sys.argv[3]
  xcl = sys.argv[4:]

if len(xcl)>1 and xcl[0]=="-x":
  xcl = xcl[1:]
else:
  xcl = []

OE = '=' in opt
OL = '<' in opt
OR = '>' in opt
OU = '[' in opt
OV = ']' in opt
OC = '-' not in opt
OX = 's' in opt
OD = '+' in opt
OH = 'h' in opt
OA = 'c' in opt

if OA:
  CRED1 = "\x1b[31;1m"
  CGRN1 = "\x1b[32;1m"
  CYEL1 = "\x1b[33;1m"
  CYEL0 = "\x1b[33m"
  CWHT1 = "\x1b[37;1m"
  CWHT0 = "\x1b[37;40m"
  CWHTX = "\x1b[30;1m"
  CCYA1 = "\x1b[36;1m"
  CMAG1 = "\x1b[35;1m"
  CRED2 = "\x1b[41;33;1m"
else:
  CRED1 = CGRN1 = CYEL1 = CYEL0 = CWHT1 = CWHT0 = CWHTX = CCYA1 = CMAG1 = CRED2 = ""

def filetxt(filename):
  f = open(filename,"rb")
  t = f.read()
  f.close()
  return t

def cmpdirs(ind,src,dst):
  for x in xcl:
    x = "/"+x
    if src.endswith(x) and dst.endswith(x):
      print ind+"- "+CWHTX+"..."+CWHT0
      return
  if not os.path.exists(src):
    print ind+CRED2+"! "+src+CWHT0
    return
  if not os.path.exists(dst):
    print ind+CRED2+"! "+dst+CWHT0
    return
  dst_files = os.listdir(dst)
  dst_files.sort()
  src_files = os.listdir(src)
  src_files.sort()
  for f in src_files:
    src_pf = os.path.join(src,f)
    if os.path.islink(src_pf):
      if f not in dst_files:
        if OU: print ind+CGRN1+"[", f+">"+CWHT0
    elif os.path.isfile(src_pf):
      if f not in dst_files:
        if OU: print ind+CGRN1+"[", f+CWHT0
      else:
        src_mt = os.stat(src_pf).st_mtime
        #  src_mts = time.strftime("%Y.%m.%d %H:%M:%S",time.localtime(src_mt))
        dst_pf = os.path.join(dst,f)
        if os.path.islink(dst_pf):
          continue
        dst_mt = os.stat(dst_pf).st_mtime
        if os.path.isdir(dst_pf):
          if OC: print ind+CCYA1+"%", f+CWHT0
          if OC: print ind+CCYA1+"%", f+"/"+CWHT0
        else:
          if src_mt == dst_mt:
            src_sz = os.stat(src_pf).st_size
            dst_sz = os.stat(dst_pf).st_size
            if src_sz != dst_sz: print ind+CMAG1+"~", f+CWHT0
            if OE: print ind+CWHT1+"=", f+CWHT0
          else:
            if OX:
              src_sz = os.stat(src_pf).st_size
              dst_sz = os.stat(dst_pf).st_size
              if src_sz == dst_sz:
                src_txt = filetxt( src_pf )
                dst_txt = filetxt( dst_pf )
                if src_txt == dst_txt:
                  continue
            if src_mt < dst_mt:
              if OR: print ind+CYEL0+">", f+CWHT0
            else:
              if OL: print ind+CYEL1+"<", f+CWHT0
  for f in dst_files:
    if f not in src_files:
      dst_pf = os.path.join(dst,f)
      if os.path.islink(dst_pf):
        if OV: print ind+CRED1+"]", f+">"+CWHT0
      elif os.path.isfile(dst_pf):
        if OV: print ind+CRED1+"]", f+CWHT0
      elif os.path.isdir(dst_pf):
        if OV: print ind+CRED1+"]", f+"/"+CWHT0
  for f in src_files:
    src_pf = os.path.join(src,f)
    if os.path.isdir(src_pf) and not os.path.islink(src_pf):
      if f not in dst_files:
        if OU: print ind+CGRN1+"[", f+"/"+CWHT0
      else:
        dst_pf = os.path.join(dst,f)
        if not os.path.isdir(dst_pf):
          if OC: print ind+CCYA1+"%", f+"/"+CWHT0
          if OC: print ind+CCYA1+"%", f+CWHT0
        else:
          if OD:
            if OH:
              print ind+"+", f
            else:
              print ind+"+", f, " \t"+CWHTX+":%s/"%src_pf+CWHT0
            cmpdirs( ind+"  ",src_pf, dst_pf )
          else:
            print ind+"+", f

cmpdirs("",src,dst)
