
import sys,os,os.path,shutil,hashlib,time
from utils import format_int
from console_output import cc,ww,F_Y,F_I,F_R,F_M,F_C,F_W

if len(sys.argv)<3:
  print( "Syntax: dirsync.py [-n|-s|-o] dir-orig dir-backup" )
  print( " -n -- don't really sync anything, just tell what's to be done" )
  print( " -s -- silent: don't say anything while working" )
  sys.exit(0)

d_orig = sys.argv[-2]
d_bkup = sys.argv[-1]
o_show = sys.argv[1]!="-s" # show
o_work = sys.argv[1]!="-n" # work
o_xlwr = True # change .xxx or .xxxx extensions to lower case

RMVD = "@@##@@"

def log( msg ): print( msg, file=logfile )

def wrt( msg ): ww( msg+"\n" )

def prt(c,t):
  if o_show:
    cc(c); wrt(t); cc(F_W)

def move_file( src, dst, l ):
  if RMVD in dst:
    m = "rm "+src[l:]
    log( m )
    if o_show:
      wrt( m )
  else:
    m = "mv "+src[l:]+" --> "+dst[l:]
    log( m )
    if o_show:
      wrt( m )
  if o_work:
    try:
      os.renames( src, dst )
    except FileExistsError as e:
      prt(F_R|F_I,str(e))
      prt(F_R,"while moving "+src[l:])
      log( "ERROR MOVING "+src[l:] )

def copy_file( src, dst, f ):
  log( "cp "+f )
  if o_show:
    wrt( "cp "+f )
  if o_work:
    p = os.path.split(dst)[0]
    if not os.access( p, os.F_OK ):
      os.makedirs( p )
    shutil.copyfile( src, dst )
    shutil.copystat( src, dst )

def get_md5( d, f ):
  fh = open(os.path.join(d,f),'rb')
  hh = hashlib.md5()
  blocksize = 10*1024*1024 # good for 99% of photos
  buf = fh.read(blocksize)
  while len(buf) > 0:
    hh.update(buf)
    buf = fh.read(blocksize)
  fh.close()
  return hh.digest()

def collect( d, subdir, rmv, d_all ):
  if subdir:
    d = os.path.join(d,subdir)
  else:
    rmv = len(d)
  n = 0
  s = 0
  d_files = os.listdir(d)
  for f in d_files:
    d_pf = os.path.join(d,f)
    if os.path.isfile(d_pf) and not os.path.islink(d_pf):
      p = os.path.join(d,f)
      a = p[rmv:]
      if o_xlwr:
        if a[-4]==".": a = a[:-4]+a[-4:].lower()
        elif a[-5]==".": a = a[:-5]+a[-5:].lower()
      d_all.append( a )
      n += 1
      s += os.stat(p).st_size
    elif os.path.isdir(d_pf) and not os.path.islink(d_pf):
      if f!=RMVD:
        n1,s1 = collect( d, f, rmv, d_all )
        n += n1
        s += s1
  return n,s

def sync( orig, bkup ):
  t0 = time.time()

  if not orig.endswith(os.sep): orig += os.sep
  orig_all = []
  no,so = collect( orig, "", 0, orig_all )
  orig_all.sort()
  t1 = time.time()
  t_orig_read = t1 - t0; t0 = t1

  if not bkup.endswith(os.sep): bkup += os.sep
  bkup_all = []
  nb,sb = collect( bkup, "", 0, bkup_all )
  bkup_all.sort()
  t1 = time.time()
  t_bkup_read = t1 - t0; t0 = t1

  nn = len(str(max(no,nb)))
  sn = len(format_int(max(so,sb)))
  prt( F_Y|F_I, "Orig %*d -- %*s" % (nn,no,sn,format_int(so)) )
  prt( F_M|F_I, "Bkup %*d -- %*s" % (nn,nb,sn,format_int(sb)) )

  STR = type('')

  # process originals - find md5, find duplicates

  orig_set = {} # md5 : name | [n1,n2...]
  dupl_cnt = 0
  for i,f in enumerate(orig_all):
    if i%50==0: ww( "%d %.1f%%"%(i,i*100.0/no) + "\r" )
    md5 = get_md5(orig,f)
    if md5 in orig_set:
      dupl_cnt += 1
      x = orig_set[md5]
      if type(orig_set[md5]) is STR:
        wrt( "** "+f+" == "+x )
        log( "** "+f+" == "+x )
        orig_set[md5] = [x,f]
      else:
        wrt( "*%d "%(len(x)+1)+f+" == "+x[0] )
        log( "*%d "%(len(x)+1)+f+" == "+x[0] )
        x.append(f)
    else:
      orig_set[md5] = f
  t1 = time.time()
  t_orig_md5 = t1 - t0; t0 = t1

  prt( F_C|F_I,"** %d duplicates          "%dupl_cnt )
  log( "** %d duplicates"%dupl_cnt )

  prt( F_C|F_I, "::"+20*" " )
  LB = len(bkup)

  # backup files

  to_del = []
  for i,f in enumerate(bkup_all):
    if i%50==0: ww( "%d %.1f%%"%(i,i*100.0/nb) + "\r" )
    md5 = get_md5(bkup,f)
    if md5 in orig_set:
      fo = orig_set[md5]
      if type(fo) is STR:
        if f==fo:
          pass #print( "==",f )
        else:
          move_file( os.path.join(bkup,f), os.path.join(bkup,fo), LB )
        del orig_set[md5]
        #orig_all.remove(fo)
      else: # LIST
        try:
          x = fo.index(f)
        except ValueError:
          x = 0
          move_file( os.path.join(bkup,f), os.path.join(bkup,fo[x]), LB )
        del orig_set[md5][x]
        if len(orig_set[md5])==1:
          orig_set[md5] = orig_set[md5][0]
        #orig_all.remove(x)
    else:
      to_del.append(f)
  t1 = time.time()
  t_bkup_move = t1 - t0; t0 = t1

  prt( F_C|F_I, ">>"+20*" " )

  orig_all = []
  for f in orig_set.values():
    if type(f) is STR:
      orig_all.append(f)
    else:
      for f1 in f:
        orig_all.append(f1)

  for f in sorted(orig_all):
    copy_file( os.path.join(orig,f), os.path.join(bkup,f), f )
  t1 = time.time()
  t_orig_copy = t1 - t0; t0 = t1

  prt( F_C|F_I, "//" )

  to_del.sort()
  for f in to_del:
    move_file( os.path.join(bkup,f), os.path.join(bkup,RMVD,f), LB )
  t1 = time.time()
  t_bkup_remv = t1 - t0; t0 = t1

  prt( F_C|F_I, "!!" )

  prt( F_W|F_I, "orig read %5.1f" % t_orig_read )
  prt( F_W|F_I, "bkup read %5.1f" % t_bkup_read )
  prt( F_W|F_I, "orig md5  %5.1f" % t_orig_md5 )
  prt( F_W|F_I, "bkup move %5.1f" % t_bkup_move )
  prt( F_W|F_I, "orig copy %5.1f" % t_orig_copy )
  prt( F_W|F_I, "bkup remv %5.1f" % t_bkup_remv )

with open( os.path.join(os.getenv("TEMP"),"dirsync.log"), "wt", encoding="utf-8" ) as logfile:
  sync( d_orig, d_bkup )

