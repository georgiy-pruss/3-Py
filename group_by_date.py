import os,sys,stat,time,shutil

dirs = {}
dd = os.listdir(".")
nn = len(dd)
for i,fl in enumerate(dd):
  st = os.stat(fl)
  md = st.st_mode
  if stat.S_ISDIR(md) or st.st_size>50000000:
    continue
  ct = st.st_ctime
  mt = st.st_mtime
  ct = min(mt,ct)
  lt = time.localtime(ct)
  di = time.strftime("%Y%m%d",lt)
  if di not in dirs:
    if os.access(di,os.W_OK):
      ds = os.stat(di)
      if stat.S_ISDIR(ds.st_mode):
        dirs[di] = True
      else:
        print( "\nProbably not dir "+di )
        sys.exit(0)
    else:
      try:
        os.mkdir( di )
      except:
        print( "\nCan't make dir "+di )
        sys.exit(0)
    dirs[di] = True
  np = os.path.join(di,fl)
  print( "\r%d of %d, %s --> %-40s" % (i+1,nn,fl,np), end="" )
  shutil.move( fl, np )
print()
