# Date in TJD format: TJD = MJD-40000 = JD-2440000.5
# http://www.csgnetwork.com/juliantruncdateconv.html
# http://en.wikipedia.org/wiki/Julian_day
# Unix range dates are uint16: 1970/1/1..2038/1/18 --> 587..25441
# All dates before 10/15/1582 are Julian! All after are Gregorian.
# There were no dates 10/5..10/14! after 10/4/1582 there was 10/15/1582.
#
# -140840 10/15/1582
#  -99999 08/09/1694
#  -32768 09/03/1868
#   -1023 08/05/1965
#       0 05/24/1968 Fr (tjd+5)%7
#       1 05/25/1968 Sa
#     587 01/01/1970
#    9999 10/09/1995 Mo
#   13735 12/31/2005 Sa
#   13965 08/18/2006 Fr   (now 13379, 586 less)
#   16383 04/01/2013
#   19999 02/24/2023
#   25441 01/18/2038
#   32767 02/08/2058
#   65535 10/28/2147
#   99999 03/08/2242

DN_NUL = 0     # Null date, can signal no date or wrong date (actually it's 05/24/1968)
DN_MIN = 587   # For unix time, may be used to check date (1970.1.1)
DN_MAX = 25441 # For unix time, may be used to check date (2038.1.18)
DN_INF = 32767 # Some big non-existing date, good for initialization of 'min()'
DN_MOON = 29.53058867 # lunar synodic month

M_DAYS = (0, 31,28, 31,30,31, 30,31,31, 30,31,30, 31)
WD_NAME = ("Sun","Mon","Tue","Wed","Thu","Fri","Sat","Sun")

def is_unix_date( dn ):
  "Checks if date (in TJD) is between 1970.1.1 and 2038.1.18"
  return DN_MIN <= dn <= DN_MAX

def is_unix_year( y ):
  "Checks if year is between 1970 and 2038"
  return 1970 <= y <= 2038

def is_leap_year( y ):
  "Checks if y is a leap year. Before 1582 Julian calendar is used!"
  if y<1582: return y%4 == 0
  return y%4 == 0 and y%100 != 0 or y%400 == 0

def days_in_ym( y, m ):
  "Return number of days in month m of year y"
  if m==2 and is_leap_year(y): return 29
  return M_DAYS[m]

def is_ymd_valid( y, m, d ):
  "Checks if there exist such a day" # Note. ymd2dn accepts any m and d!
  if d<1 or m<1 or m>12: return False
  if d<=M_DAYS[m]: return True
  if d>29: return False
  return is_leap_year(y)

from time import localtime, time, timezone, daylight

def current_dn():
  "Return current day number, ymd2dn( today )"
  #return int( time() / 86400 ) + 587 --------- this was UTC/GMT!
  return ymd2dn(*localtime()[:3])

def current_ymd():
  "Return current y,m,d"
  return localtime()[:3]

def current_hms():
  "Return current h,m,s"
  return localtime()[3:6]

def current_dt():
  "Return current y,m,d,h,m,s"
  return localtime()[:6]

def current_YMD():
  "Return current date as string YYYY.MM.DD"
  return dn2s(current_dn())

def current_HMS():
  "Return current time as string HH:MM:SS"
  return "%02d:%02d:%02d"%current_hms()

def current_DT():
  "Return current date and time as string YYYY.MM.DD HH:MM:SS"
  return current_YMD()+" "+current_HMS()

def current_tz():
  "Return offset from UTC/GMT in hours, EST -5, EDT -4"
  return -timezone/36e2 + (daylight and 1 or 0)

def ymd2dn( year, month, day ):
  "Convert date to TJD number. Month and day may be quite wild."
  # Years BC: 0 = 1 BC, -1 = 2 BC, -2 = 3 BC, etc
  b = 0
  if month > 12:
    year = year + month//12
    month = month%12
  elif month < 1:
    month = -month
    year = year - month//12 - 1
    month = 12 - month%12
  #if year > 0:      Python: x//y is ceil(x/y), so no need for correction
  #  yearCorr = 0    (was: return (1461*year - yearCorr)//4 + ...)
  #else:
  #  yearCorr = 3
  if month < 3:
    year -= 1
    month += 12
  if year*10000 + month*100 + day > 15821014:
    b = 2 - year//100 + year//400
  return 1461*year//4 + 306001*(month + 1)//10000 + day + b - 719006

def dn2ymd( dn ):
  "Convert TJD day number to tuple (year, month, day)"
  # Probably needs some correction for dates before 1.1.1
  #if dn==0:
  #  return (0,0,0)
  #assert DN_MIN <= dn <= DN_MAX
  jdi = dn + 2440000
  if jdi < 2299160: # (1582, 10, 15)
    b = jdi + 1525
  else:
    alpha = (4*jdi - 7468861)//146097
    b = jdi + 1526 + alpha - alpha//4
  c = (20*b - 2442)//7305
  d = 1461*c//4
  e = 10000*(b - d)//306001
  day = b - d - 306001*e//10000
  if e < 14: month = e - 1
  else:      month = e - 13
  if month > 2: year = c - 4716
  else:         year = c - 4715
  return (year, month, day)

def dn2s( dn ):
  "Convert date day number to string YYYY.MM.DD"
  return "%04d.%02d.%02d" % dn2ymd(dn)

def s2dn( s ):
  "Parse string YYYY.MM.DD to date day number"
  y,m,d = s.split('.')
  return ymd2dn( int(y), int(m,10), int(d,10) )

def dn2weekday( dn ):
  "Convert date day number to weekday 0..6 (Sun..Sat)"
  return (dn+5) % 7

def dn2weekday1( dn ):
  "Convert date day number to weekday 1..7 (Mon..Sun)"
  return (dn+4) % 7 + 1

def dn2cjd( dn ):
  "Return Chronological Julian Date -- CJD 0 is Monday 1 Jan 4713 BC Julian"
  return dn+2440001 # JDN = CJD - 0.5 in UTC

def dn2mjd( dn ):
  "Return Modified Julian Date -- MJD 0 started @ 00:00 GMT on Wed 1858/11/17"
  return dn+40000 # MJD = JDN - 2400000.5, JDN = MJD + 2400000.5

def dn2jdn( dn, tz=0 ):
  """Return Julian Day Number -- JDN 0.0 is noon GMT Mon 1/1 4713 BC Julian
  Optionally adjust for the time zone tz (in hours) e.g. EST = -5, EDT = -4
  To calculate JDN considering time and time zone, use this calls:
  dn2jdn( current_dn() + hms2d(*current_hms()), current_tz() )"""
  return dn+2440000.5-tz/24.0

def jdn2dn( jdn, tz=0 ):
  "Return dn from Julian Day Number (and optionally convert to local tz)"
  return jdn-2440000.5+tz/24.0

def jdn2moonphase( jdn ):
  """Return approx moon phase, in days. Error is +-0.3 day, max +-0.6 day.
  Use dn2jdn( current_dn() + hms2d(*current_hms()), current_tz() ) to calculate
  the current julian day number"""
  return (jdn-2449128.59)%DN_MOON

def add_day( y,m,d, n=1 ):
  "Increment y,m,d by n days (can be negative, default 1)"
  return dn2ymd( ymd2dn(y,m,d) + n )

def ensure_workday( dn ):
  "Return TJD corresp. to Monday if argument is Friday or Saturday"
  "ToDo: add USA holydays"
  wd = dn2weekday(dn)
  if wd==0: return dn+1
  if wd==6: return dn+2
  return dn

def nth_day_of_month( n, w, m, y ):
  """Return n-th weekday in given month (as dn). Zero for the last day.
  E.g. 1st Sunday in April 2011 is April 3 (1,0,4,2011 --> 2011.4.3)
  Last Friday in 2011 is on December 30 (0,5,12,2011 --> 2011.12.30)
  """
  dn = ymd2dn(y,m,1)
  wd = dn2weekday(dn)
  d = w-wd+1
  if d<1: d += 7
  dn += d-1
  if n>0:
    dn += (n-1)*7
  else: # n==0
    dn += 28
    y1,m1,d1 = dn2ymd(dn)
    if m1!=m: dn -= 7
  return dn

def hms2d( h,m,s ):
  "Return h/24 + m/24*60 + s/24*3600"
  return ((s/60.0+m)/60.0+h)/24.0

def d2hms( d ):
  "Return 0<=d<1 --> h,m,s"
  d *= 24; h = int(d); d -= h;
  d *= 60; m = int(d); d -= m;
  return (h,m,d*60)


# ==============================================================================

if __name__ == "__main__":
  from sys import argv
  if len(argv)==2 and argv[1]=="012345": # TEST *********************************

    # TEST 1 - some predefined dates

    T = [
    (1, -99999, (1694, 8, 9)),
    (5, -46529, (1841, 1, 1)),
    (3, -40000, (1858,11,17)),
    (4, -32768, (1878, 9, 5)),
    (4,  -1023, (1965, 8, 5)),
    (5,      0, (1968, 5,24)),
    (6,      1, (1968, 5,25)),
    (4,    587, (1970, 1, 1)),
    (1,   9999, (1995,10, 9)),
    (6,  13735, (2005,12,31)),
    (5,  13965, (2006, 8,18)),
    (1,  16383, (2013, 4, 1)),
    (5,  19999, (2023, 2,24)),
    (1,  25441, (2038, 1,18)),
    (5,  32767, (2058, 2, 8)),
    (6,  65535, (2147,10,28)),
    (2,  99999, (2242, 3, 8))]

    for w,j,(y,m,d) in T:
      nw = (j+7000005) % 7
      if w != nw:
        print( j,'calculated:',nw,'instead of',w )
      ny,nm,nd = dn2ymd( j )
      if (ny,nm,nd) != (y,m,d):
        print( j,'calculated:',ny,nm,nd,'instead of',y,m,d )

    # TEST 2 - all dates from 1/1 5600 BC thru 12/31 9999 AD

    # -2440001 -4712/01/01 Mon (+2453979d +6718.63y) [4713BC JD 0 started at noon]
    #  -718578  0000/12/31 Fri ( +732556d +2005.63y) [   1BC Julian -- B.C. ended]
    #  -718577  0001/01/01 Sat ( +732555d +2005.63y) [   1AD Julian -- A.D. start]
    #  -134187  1601/01/01 Mon (Greg) ANSI COBOL 85 & Quattro Pro Day 1. MS filedate
    #   -46529  1841/01/01 Fri (  +60507d +165.66y) ANSI MUMPS $Horolog Day 1
    #   -40000  1858/11/17 Wed (  +53978d +147.78y) MJD 0, CJD 2400001
    # See http://www.merlyn.demon.co.uk/critdate.htm for other dates

    from time import clock
    c = clock()
    k = -2763978 # 12/31 5601 BC
    n = 0
    for y in range(-5599,10000): # 5600 BC, 5599 BC, 5598 BC, ..., 9999 AD
      #print "\r",y,
      for m in range(1,12+1):
        for d in range(1,days_in_ym(y,m)+1):
          j = ymd2dn( y,m,d )
          w = (j+7000005) % 7
          yy,mm,dd = dn2ymd( j )
          if not (yy==y and mm==m and dd==d and k+1==j):
            print( "\r",y,m,d,"==>",j,"(%s)" % k,WD_NAME[w],"==>",yy,mm,dd )
          if (y,m)==(1582,10) and d in (4,16):
            print( "\r",y,m,d,"==>",j,"(%s)" % k,WD_NAME[w],"==>",yy,mm,dd, "OK" )
          k = j
          n += 1
    print( "OK for", n, "dates" ) # OK for 5697471 dates (years -5599..9999)
    print( "%.3f s elapsed" % (clock() - c) ) # 89.2 s 56.1 s with psyco 52.9 w/o print
    '''
    1582 10  4 ==> -140841 (-140842) Thu ==> 1582 10  4 OK

    1582 10  5 ==> -140840 (-140841) Fri ==> 1582 10 15
    1582 10  6 ==> -140839 (-140840) Sat ==> 1582 10 16
    1582 10  7 ==> -140838 (-140839) Sun ==> 1582 10 17
    1582 10  8 ==> -140837 (-140838) Mon ==> 1582 10 18
    1582 10  9 ==> -140836 (-140837) Tue ==> 1582 10 19
    1582 10 10 ==> -140835 (-140836) Wed ==> 1582 10 20
    1582 10 11 ==> -140834 (-140835) Thu ==> 1582 10 21
    1582 10 12 ==> -140833 (-140834) Fri ==> 1582 10 22
    1582 10 13 ==> -140832 (-140833) Sat ==> 1582 10 23
    1582 10 14 ==> -140831 (-140832) Sun ==> 1582 10 24

    1582 10 15 ==> -140840 (-140831) Fri ==> 1582 10 15
    1582 10 16 ==> -140839 (-140840) Sat ==> 1582 10 16 OK

    OK for 5697471 dates
    43.466 s elapsed -- AMD Phenom 8450 X3
    '''

"""
j = dn2jdn( current_dn() + hms2d(*current_hms()), current_tz() )
mp = jdn2moonphase(j)
np = DN_MOON-mp
mph = nph = ""
if mp<1: mph = "/%.1fh"%(mp*24)
if np<1: nph = "/%.1fh"%(np*24)
print("%.1f%% %.2f%s (%.2f%s)"%(mp*100/DN_MOON,mp,mph,np,nph))
"""

# EOF
