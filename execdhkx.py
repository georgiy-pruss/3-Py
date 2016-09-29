# Execute DH key exchange
# Choose password, then get public derivative of the password, then
# exchange these derivatives, then you'll have your key for encryption
# For more on DHKX, see dhkx.py

import dhkx, hashlib

def enter_kind():
  txt = """Choose your key (password) type:
  1 - decimal digits (21+ digits recommended)
  2 - hexadecimal (18+ hex.digits recommended)
  3 - alphanumeric case-insensitive (14)
  4 - alphanumeric case-sensitive (12)
  5 - any printable ASCII (11)"""
  while "password kind entering":
    print( txt )
    k = input( "Enter number: " )
    if k in ("1","2","3","4","5"): return int(k)

def chk_kind( k, p ):
  if k==1 and p.isdigit(): return True
  if k==2 and p.isalnum():
    for c in p:
      if c not in "0123456789abcdefABCDEF": return False
    return True
  if (k==3 or k==4) and p.isalnum(): return True
  if k==5: return True
  return False

def enter_pwd( k ):
  while "password entering":
    p = input( "Enter password: " )
    if len(p)>0 and not chk_kind( k, p ):
      print( "Bad character" )
      continue
    if len(p)<3: # well, maybe not needed, maybe confirmation...
      print( "Too short" )
      continue
    return p

def cvt_s36_to_n( p ): # 36 = 0..9 A..Z i.e. 10+26
  n = 0
  for c in p.upper():
    if '0'<=c<='9': n=n*36+ord(c)-ord('0')
    elif 'A'<=c<='Z': n=n*36+ord(c)-ord('A')+10
    else: pass # ignore other chars
  return n

def cvt_s62_to_n( p ): # 52 = 0..9 A..Z a..z i.e. 10+26+26
  n = 0
  for c in p:
    if '0'<=c<='9': n=n*62+ord(c)-ord('0')
    elif 'A'<=c<='Z': n=n*62+ord(c)-ord('A')+10
    elif 'a'<=c<='z': n=n*62+ord(c)-ord('a')+36
    else: pass # ignore other chars
  return n

def cvt_s95_to_n( p ): # 95 = spc (32) incl till del (127) excl
  n = 0
  for c in p:
    assert 32<=ord(c)<=126
    n=n*95+ord(c)-32 # ord(' ')
  return n

def cvt_n_to_s62( n ):
  s = ''
  while n!=0:
    d = n%62
    if d>=36: s = (chr(ord('a')+d-36)) + s
    elif d>=10: s= (chr(ord('A')+d-10)) + s
    else: s = (chr(ord('0')+d)) + s
    n = n//62
  return s

def cvt_pwd_to_n( k, p ):
  if k==1: return int(p)
  if k==2: return int(p,16)
  if k==3: return cvt_s36_to_n(p)
  if k==4: return cvt_s62_to_n(p)
  if k==5: return cvt_s95_to_n(p)
  assert False

def parse( s ):
  return cvt_s62_to_n( s.replace(" ", "").replace("\n", "") )
  # it was either integer or 62-based
  #for c in 'abcdefghijklmnopqrstuvwxyz':
  #  if c in s or c.upper() in s:
  #    return cvt_62( s )
  #return int(s) # it's a number

def main():
  try:
    k = enter_kind()
    p = enter_pwd( k )
    n = cvt_pwd_to_n(k,p)
    g = dhkx.make_gx( n )
    print()
    print( 'Your number G (not secret):', cvt_n_to_s62(g) )
    print( 'Now send this G to your party' )
    print()
    print( 'And receive another G from your party' )
    f = input( 'Enter it here: ' )
    b = parse( f )
    c = dhkx.make_key( b, n )
    z = cvt_n_to_s62( c )
    print()
    print( 'Your common secret password:', z )
    h = hashlib.md5()
    h.update( z.encode('ascii') )
    print( 'Its MD5:', h.hexdigest() )
  except EOFError:
    pass

main()
