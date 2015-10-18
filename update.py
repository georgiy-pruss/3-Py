#!/usr/bin/python

import time,sys,shutil,os,os.path

if len(sys.argv) < 3:
  print "Syntax: update.py [opt] dir-from dir-to [dir-to...]"
  print "opt:"
  print "  -c  only compare files present in both from/to, don't copy them"
  print "  -a  overwrite all files present in both from/to, no time check"
  print "  -u  add only files unique in dir-from to dir-to"
  sys.exit(0)

anyway  = sys.argv[1]=="-a"
onlycmp = sys.argv[1]=="-c"
unique  = sys.argv[1]=="-u"
opt = anyway or onlycmp or unique
src = opt and sys.argv[2] or sys.argv[1]
dsts= opt and sys.argv[3:] or sys.argv[2:]
print "\nFrom:",src
errs = 0
for dst in dsts:
  print "\nTo:",dst
  if not os.access(dst,os.R_OK):
    print "!","Does not exist"
    continue
  if not os.path.isdir(dst):
    print "!","Not a directory"
    continue
  if not unique:
    dst_files = os.listdir(dst)
    dst_files.sort()
    for f in dst_files:
      pf = os.path.join(dst,f)
      if os.path.isfile(pf) and not os.path.islink(pf):
        mt = os.stat(pf).st_mtime
        src_pf = os.path.join(src,f)
        if os.path.isfile(src_pf) and not os.path.islink(src_pf):
          src_mt = os.stat(src_pf).st_mtime
          src_mts = time.strftime("%Y.%m.%d %H:%M:%S",time.localtime(src_mt))
          mts = time.strftime("%Y.%m.%d %H:%M:%S",time.localtime(mt))
          if anyway or src_mt > mt:
            if not onlycmp:
              print src_mts, "-->", mts, f
              try:
                shutil.copyfile( src_pf, pf )
              except IOError, exc:
                print "!",exc
                errs += 1
            else:
              print src_mts, ">", mts, f
          elif onlycmp:
              print src_mts, src_mt < mt and "<" or "=", mts, f
  else:
    dst_files = os.listdir(dst)
    src_files = os.listdir(src)
    src_files.sort()
    for f in src_files:
      src_pf = os.path.join(src,f)
      if os.path.isfile(src_pf) and not os.path.islink(src_pf):
        if f in dst_files:
          continue
        print "-->", f
        try:
          shutil.copyfile( src_pf, os.path.join(dst,f) )
        except IOError, exc:
          print "!",exc
          errs += 1
if errs>0:
  print errs,"errors"
