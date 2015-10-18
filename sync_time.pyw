import urllib.request, urllib.parse, urllib.error, time, re, os, math

def ask_utc_time( tzoffs, tzname ):
  """Get time form the Internet. Return "HH:MM:SS" or empty string if any failure."""
  #url = "http://tycho.usno.navy.mil/cgi-bin/timer.pl"
  t1 = t2 = math.floor(time.time() * 1000)
  url = "http://time.is/t/?en.0.110.262.0p.%d.%s.%d.%d" % (-tzoffs, tzname, t1, t2)
  try:
    doc = urllib.request.urlopen(url).read().decode("utf-8")
    # ...<BR>Feb. 15, 13:31:17 UTC\t\tUniversal Time\n...
    # m = re.search("\s+(\\d\\d:\\d\\d:\\d\\d)\\s+UTC\s+Universal Time",doc)
    m = re.search("([0-9]+)",doc)
    # if m: return m.group(1) # 12:02:54
    if m: return m.group(1) # unix-time
  except:
    pass
  return ''

def synch_time():
  """Get time from Internet, use os.system to execute 'time h:m:s', return message if ok or not"""
  offset = time.timezone;
  if time.daylight and time.localtime().tm_isdst: offset -= 3600
  time_ut = ask_utc_time(offset//60,"Europe/Kiev")
  if time_ut:
    #h,m,s = time_str.split(":")
    #seconds = int(h,10)*3600 + int(m,10)*60 + int(s,10)
    seconds = int(time_ut)//1000
    #localtm = math.floor(time.time()) # just for control
    seconds = (seconds - offset) % 86400
    h = seconds//3600
    m = seconds//60%60
    s = seconds%60
    try:
      before = time.time()
      os.system( "time %02d:%02d:%02d" % (h,m,s) ) # do synchronize!
      delta = time.time() - before
      return "The time is %02d:%02d:%02d\nCorrected by %.1f sec" % (h,m,s,delta)
    except:
      pass
  return 'Not synchronized'

if __name__ == "__main__":
  from win32ui import MessageBox
  msg = synch_time()
  MessageBox( msg, "synch_time" )

# EOF
