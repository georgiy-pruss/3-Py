#!/bin/python3
"""
Base Type extensions (see bt.txt)                  20120425-050625

list   n abs fold(f[v])  s i f j(s='') a(x)        match      s i
tuple  n     fold        s i f j(s='')             range      l
dict   n           k v         j(s=',',p=':')      generator  l
float    abs deg         s i f rnd                 object     isa
int      abs deg r x X b s i f rnd
bytes  n xor(b) xx x X b s
str    n        xx     b
str    pad(n,c=' ') fit(n,c=' ') s(x) e(x) l u k p ints c(x) f(x) r(*xy) m(x) mm(x) sub(x,y) fetch()
strfn  _n _f/r/w/x/d _t _dir _del() _lines _data[=x] _rd([m,e]) _wr(t[m,e]) _o([m,e]) _abspath _bn _dn

TIME (UT,JD,ZT,CT,TJD,SEC,YMD,HMS,DHMS,WDHMS,TZ,DST,WD,YD)

list/tuple  t d wd yd     e           c([tz[,d]]) z([tz[,d]])
int/float   t   wd yd ymd   [wd]hms j c([tz[,d]]) z([tz[,d]])  (no float.wd,yd,ymd)
str         t d ft([t])

FNS: pad(s,n[,c]) fit(s,n[,c]) repl(s,p1,t1[,p2,t2]...) hms(t) dhms(t) wdhms(t)

"""

import re,random,time,os,urllib2
from tjd import ymd2dn,dn2ymd
import typehack

def _i_rnd(n,m=None):
  if m: return random.randrange(n,m)
  return random.randrange(0,n)

def _s_xx(x):
  x = x.sub("[^0-9a-fA-F]","") # remove extra chars
  return bytes(int(x[i:i+2],16) for i in range(0,x.n,2)) # bytes.fromhex(s) in P3

def _b_xx(x):
  x = re.sub(b"[^0-9a-fA-F]",b"",x)
  return bytes(int(x[i:i+2],16) for i in range(0,x.n,2))

def _b_xor(x,y):
  """xor for bytes"""
  xn,yn = x.n,y.n
  if xn<yn: x=pad(x,yn,b'\0')
  elif yn<xn: y=pad(y,xn,b'\0')
  return bytes(xx^yy for xx,yy in zip(x,y))

def _a_fold(x,fn,v=0):
  for xx in x: v = fn(v,xx)
  return v

def _f_load(f):
  with open(f,"rb") as h: t=h.read()
  return t

def _f_save(f,t):
  with open(f,"wb") as h: h.write(t)

def _f_read(f,m="rt",e="utf-8"):
  with open(f,m,encoding=e) as h: t=h.read()
  return t

def _f_write(f,t,m="wt",e="utf-8"):
  with open(f,m,encoding=e) as h: x=h.write(t)
  return x

# -----------------------------------------------------------

def repl(x,*p):
  for i in range(0,p.n,2):
    x = x.replace(p[i],p[i+1])
  return x

def fit(x,n,c=' '):
  """pad string up to length |n| with char c. truncate string if shorter."""
  if n<0:
    return fit(x[::-1],-n,c[::-1])[::-1]
  if x.n>=n: return x[:n]
  d = n-x.n
  m = (d+c.n-1)//c.n
  return x + (m*c)[:d]

def pad(x,n,c=' '):
  """pad string up to length |n| with char c. don't truncate string if shorter."""
  if n<0:
    if x.n>-n: return x
    return pad(x[::-1],-n,c[::-1])[::-1]
  if x.n>n: return x
  d = n-x.n
  m = (d+c.n-1)//c.n
  return x + (m*c)[:d]

def geturl(u): # see http://docs.python.org/py3k/howto/urllib2.html
  try: return urllib2.urlopen(u).read()
  except urllib.URLError: return None

def hms(x):
  m,s = divmod(x,60); h,m = divmod(int(m),60)
  return (h,m,s)

def dhms(x):
  m,s = divmod(x,60); h,m = divmod(int(m),60); d,h = divmod(h,24)
  return (d,h,m,s)

def wdhms(x):
  m,s = divmod(x,60); h,m = divmod(int(m),60); d,h = divmod(h,24); w,d = divmod(d,7)
  return (w,d,h,m,s)

list.n = property(list.__len__)
tuple.n = property(tuple.__len__)
dict.n = property(dict.__len__)
str.n = property(str.__len__)
bytes.n = property(bytes.__len__)

list.a = list.append
list.j = tuple.j = lambda x,s='':s.join(str(i) for i in x)
list.fold = tuple.fold = _a_fold

dict.j = lambda x,s=',',p=':':s.join("%s%s%s"%(i,p,j) for i,j in x.items())
dict.k = property(lambda x:x.keys())
dict.v = property(lambda x:x.values())

list.i = property(lambda x:[int(e) for e in x])
list.f = property(lambda x:[float(e) for e in x])
list.s = property(lambda x:[str(e) for e in x])

tuple.i = property(lambda x:tuple(int(e) for e in x))
tuple.f = property(lambda x:tuple(float(e) for e in x))
tuple.s = property(lambda x:tuple(str(e) for e in x))

list.abs = property(lambda x:[abs(e) for e in x])

str.e = str.endswith          # all these could be for bytes too. add when need
str.s = str.startswith
str.l = property(str.lower)
str.u = property(str.upper)
str.k = property(str.split)
str.p = property(str.strip)
str.c = str.count
str.f = str.find
str.r = repl
str.m = lambda x,p:re.search(p,x)
str.mm = lambda s,p:re.findall(p,s)
str.sub = lambda x,p,q:re.sub(p,q,x)
str.pad = pad
str.fit = fit
str.ints = property(lambda x:re.findall("[-+]?\\d+",x).i)
str.fetch = geturl

_mt = type(re.match("",""))
_mt.s = property(lambda x:x.group())
_mt.i = property(lambda x:x.start())

str.xx = property(_s_xx)
str.b = property(lambda x:x.encode('utf-8'))

bytes.xx = property(_b_xx)
bytes.x = property(lambda x:''.join("%02x"%c for c in x))
bytes.X = property(lambda x:''.join("%02X"%c for c in x))
bytes.s = property(lambda x:x.decode('utf-8'))
bytes.xor = _b_xor

int.x = property(lambda x:"%x"%x)
int.X = property(lambda x:"%X"%x)
int.b = property(lambda x:"{0:b}".format(x))
int.f = property(float)
int.r = property(range)           # N.r --> range
int.rnd = property(_i_rnd)
int.deg = float.deg = property(lambda x:0.017453292519943295*x) # 57.295779513082322

# in 2.7, there's also 'long'

int.i = long.i = float.f = bytes.b = property(lambda x:x) # self, to allow s.b and b.b, etc
int.s = long.s = float.s = int.s = property(str)
int.abs = long.abs = float.abs = property(abs)

long.x = property(lambda x:"%x"%x)
long.X = property(lambda x:"%X"%x)
long.b = property(lambda x:"{0:b}".format(x))
long.f = property(float)
long.r = property(range)           # N.r --> range
long.rnd = property(_i_rnd)
long.deg = property(lambda x:0.017453292519943295*x) # 57.295779513082322

float.i = property(int)
float.rnd = property(lambda x:x*random.random())

type(range(0)).l = property(list) # N.r.l --> list
type(_ for _ in []).l = property(list) # generator --> list

object.isa = lambda o,c:isinstance(o,c)

# file

str._dir = property(lambda x:os.listdir(x))
str._f = property(lambda x:os.access(x,os.F_OK))
str._r = property(lambda x:os.access(x,os.R_OK))
str._w = property(lambda x:os.access(x,os.W_OK))
str._x = property(lambda x:os.access(x,os.X_OK))
str._d = property(os.path.isdir)
str._n = property(lambda x:os.stat(x).st_size)
str._t = property(lambda x:os.stat(x).st_mtime)
str._del = lambda x:os.unlink(x)
str._o = lambda x,m="rt",e="utf-8":open(x,m,encoding=e)
str._lines = property(lambda x:open(x,"rt",encoding="utf-8").readlines())
str._data = property(_f_load,_f_save)
str._rd = _f_read
str._wr = _f_write

str._abspath = property(os.path.abspath)
str._dn = property(os.path.dirname)
str._bn = property(os.path.basename)

# TIME stuff

def _norm_tz(x): # +-... --> +-SEC
  if -15<=x<=15: return x*3600     # hours
  if x<=-1800 or 1800<=x: return x # seconds
  if x<0: return -_norm_tz(-x)     # negative
  h,m = divmod(x,100)              # hhmm
  return (h*60+m)*60

def _fmt_tz(x,d=""): # SEC --> shhmm or shhdmm
  s = "+"
  if x<0:
    s = "-"; x = -x
  h,m = divmod(x//60,60)
  return "%s%02d%s%02d" % (s,h,d,m)

def _a_zc2t(t): # (y m d H M [S tz dst...]) or (tjd sec [tz dst])
  if t.n==0: return time.time()
  if t.n==3: return (t[0]-587)*864e2 + t[1] - _norm_tz(t[2])
  if t.n==4: return (t[0]-587)*864e2 + t[1] - _norm_tz(t[2]) - _norm_tz(t[3])
  if t.n==2: return (t[0]-587)*864e2 + t[1] + time.timezone - _norm_tz(time.daylight)
  if t.n==1: assert False,"t must be empty, or 2..4 items of CT, or 5..8+ items of ZT"
  ymd,t = t[:3],list(t[3:])
  if t.n==2: t.append(0)
  if t.n==3: t += [-time.timezone,time.daylight]
  hms,tz,dst = t[:3],t[3],0
  if t.n>4: dst = t[4]
  return (ymd2dn(*ymd)-587)*864e2 + _bt_hms2i(hms) - (_norm_tz(tz)+_norm_tz(dst))

def _t_2c(t,tz=None,dst=0):
  if tz is None:
    tz = _norm_tz(-time.timezone)
    dst = _norm_tz(time.daylight)
  elif tz is Ellipsis:
    tz = _norm_tz(-time.timezone)
    dst = _norm_tz(dst)
  else:
    tz = _norm_tz(tz)
    dst = _norm_tz(dst)
  t += tz + dst
  return (int(t//86400)+587,t%86400,tz,dst)

def _t_2z(t,tz=None,dst=0):
  c = _t_2c(t,tz,dst)
  dt = c[0].ymd
  tm = c[1].hms
  return [dt[0],dt[1],dt[2],tm[0],tm[1],tm[2],c[2],c[3]]

def _a_zc2z(t,tz=None,dst=0):
  # TODO
  if t.n==4:
    dt = t[0].ymd
    tm = t[1].hms
    return [dt[0],dt[1],dt[2],tm[0],tm[1],tm[2],t[2],t[3]]
  assert t.n==8
  if type(t)==tuple: return list(t)
  return t

def _a_zc2c(t,x=None):
  # TODO
  if t.n==4: return tuple(t)
  assert t.n==8
  dt = t[:3].d
  tm = t[3:6].e
  return (dt,tm,t[6],t[7])

def _bt_ymd2dt(x):
  if not x: return ymd2dn(*time.localtime()[:3])
  return ymd2dn(*x)

def _bt_ymd2yd(y,m,d):
  return (y,m,d).d - (y,1,0).d

def _bt_d2yd(x):
  y,m,d = dn2ymd(x)
  return x - (y,1,0).d

def _bt_hms2i(x):
  if x.n==5: return (((x[0]*7+x[1])*24+x[2])*60+x[3])*60+x[4]
  if x.n==4: return ((x[0]*24+x[1])*60+x[2])*60+x[3]
  if x.n==3: return (x[0]*60+x[1])*60+x[2]
  if x.n==2: return x[0]*60+x[1]
  assert x.n==1; return x[0]

def _bt_s2u(x):
  if x=="": return time.time()
  x = x.ints
  for i in min(6,x.n).r: x[i] = abs(x[i])
  return _a_zc2t(x)

def _bt_s2dn(x): # 3 ints in x!
  if x=="": return ymd2dn(*time.localtime()[:3])
  return ymd2dn(*x.ints.abs)

# English names, can be used
date_data_e="Sun Mon Tue Wed Thu Fri Sat".k
date_data_E="Sunday Monday Tuesday Wednesday Thursday Friday Saturday".k
date_data_o="Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".k
date_data_O="January February March April May June July August September October November December".k
# User data, can be changed
date_data = {"D":"$Y.$m.$d", "T":"$H:$M:$S", "p":("AM","PM"), "P":("","DST"),
    "a":date_data_e[:], "A":date_data_E[:], "b":date_data_o[:], "B":date_data_O[:] }

def _s_fmttime(x,t=None):
  if x=="": x = "$e, $d $o $Y $T $Z" # "Thu, 28 Jun 2001 14:17:15 +0000"
  if t==None:
    t = ''.t # current time
  wd = yd = None
  if type(t) in (int,float):
    y,m,d,H,M,S,tz,dst = t.z(); ymd=(y,m,d)
  elif t.n==4:
    y,m,d = t[0].ymd; H,M,S = t[1].hms; tz,dst = t[2],t[3]; ymd=t[0]
  elif t.n>=8:
    y,m,d,H,M,S,tz,dst = t[:8]; ymd=t[:3]
    if t.n>=9:
      wd = t[8]
      if t.n==10: yd = t[9]
  else:
    assert False,"???"+str(t)
  if wd is None: wd = ymd.wd
  if yd is None: yd = ymd.yd
  tz = _norm_tz(tz)
  ms,S = int(S*1000)%1000,int(S)
  x = x.r("$D",date_data["D"],"$T",date_data["T"])
  x = x.r("$Y","%04d"%y,"$y","%02d"%(y%100),"$m","%02d"%m,"$d","%02d"%d)
  x = x.r("$H","%02d"%H,"$M","%02d"%M,"$S","%02d"%S,"$t","%03d"%ms)
  x = x.r("$h","%02d"%((H+11)%12+1),"$p","%s"%date_data["p"][int(H>=12)])
  x = x.r("$a",date_data["a"][wd],"$A",date_data["A"][wd])
  x = x.r("$b",date_data["b"][m-1],"$B",date_data["B"][m-1])
  x = x.r("$e",date_data_e[wd],"$E",date_data_E[wd])
  x = x.r("$o",date_data_o[m-1],"$O",date_data_O[m-1])
  x = x.r("$Z",_fmt_tz(tz),"$z",_fmt_tz(tz,":"),"$w",wd.s)
  x = x.r("$P",date_data["P"][int(dst!=0)],"$n","%03d"%_bt_ymd2yd(y,m,d))
  return x.r("$s","$")
  #p = xx.m("\\$[AaBbDdEeHhMmnOoPpSsTtwYyZz]")
  #while p:
  #  if p.s[1]=='a': xx = xx.r("$a",....)
  #  if p.s[1]=='A': xx = xx.r("$A",....)
  #  p = xx.m("\\$[AaBbDdEeHhMmnOoPpSsTtwYyZz]")

# time

int.j = float.j = property(lambda x:x/864e2+2440587.5)
int.t = float.t = property(lambda x:(x-2440587.5)*864e2)
int.z = float.z = _t_2z   # UT(tzx) --> [y m d H M S tzo dst]
int.c = float.c = _t_2c   # UT(tzx) --> [tjd sec tzo dst]
int.ymd = property(dn2ymd)
int.wd = property(lambda x:(x+5)%7)
int.yd = property(_bt_d2yd)
int.hms = float.hms = property(hms)
int.dhms = float.dhms = property(dhms)
int.wdhms = float.wdhms = property(wdhms)

list.t = tuple.t = property(_a_zc2t)  # [] or CT or ZT --> UT
list.z = tuple.z = _a_zc2z
list.c = tuple.c = _a_zc2c
list.d = tuple.d = property(_bt_ymd2dt)
list.wd = tuple.wd = str.wd = property(lambda x:x.d.wd)
list.yd = tuple.yd = property(lambda x:_bt_ymd2yd(*x))
list.e = tuple.e = property(_bt_hms2i)

str.t = property(_bt_s2u)
str.d = property(_bt_s2dn)
str.ft = _s_fmttime # ''.ft([t]) --> Www Mmm dd HH:MM:SS YYYY; oherwise strftime

# EOF
