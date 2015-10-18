import sys,hashlib,binascii,glob,os.path

if len(sys.argv)<2:
  print("chksum.py [+64] [md5] files...")
  sys.exit(0)

CRCTableh = [0] * 256
CRCTablel = [0] * 256

def init_crc_tables():
  POLY64REVh = 0xd8000000
  for i in range(256):
    partl = i
    parth = 0
    for j in range(8):
      rflag = partl & 1
      partl >>= 1
      if parth & 1:
        partl |= 1 << 31
      parth >>= 1
      if rflag:
        parth ^= POLY64REVh
    CRCTableh[i] = parth;
    CRCTablel[i] = partl;

init_crc_tables()

def crc64update( s, crch, crcl ):
  for item in s:
    shr = (crch & 0xFF) << 24
    temp1h = crch >> 8
    temp1l = (crcl >> 8) | shr
    tableindex = (crcl ^ item) & 0xFF
    crch = temp1h ^ CRCTableh[tableindex]
    crcl = temp1l ^ CRCTablel[tableindex]
  return crch, crcl

assert "%08x%08x" % crc64update(b"IHATEMATH",0,0) == "e3dcadd69b01add1"

#print( hashlib.algorithms_guaranteed )
#print( hashlib.algorithms_available )

def print_chksums( fnm, with_crc64, only_md5 ):
  if not only_md5:
    print( "\n"+fnm+":\n" )

  inp = open(fnm,"rb")

  PART_SIZE = 1024*1024  # 1 MiB
  txt = inp.read( PART_SIZE )

  h_md5 = hashlib.new( 'md5', txt )
  if not only_md5:
    h_crc32 = binascii.crc32(txt)
    h_md4 = hashlib.new( 'md4', txt )
    if with_crc64: h64,l64 = crc64update( txt, 0, 0 )
    h_sha = hashlib.new( 'sha', txt )
    h_sha1 = hashlib.new( 'sha1', txt ) # == 'DSA' 'DSA-SHA' 'ecdsa-with-SHA1' 'dsaWithSHA' 'dsaEncryption'
    h_sha224 = hashlib.new( 'sha224', txt )
    h_sha256 = hashlib.new( 'sha256', txt )
    h_sha384 = hashlib.new( 'sha384', txt )
    h_sha512 = hashlib.new( 'sha512', txt )
    h_ripemd160 = hashlib.new( 'ripemd160', txt )
    h_whirlpool = hashlib.new( 'whirlpool', txt )

  while len(txt) == PART_SIZE:

    txt = inp.read( PART_SIZE )

    h_md5.update( txt )
    if not only_md5:
      h_crc32 = binascii.crc32(txt,h_crc32)
      h_md4.update( txt )
      if with_crc64: h64,l64 = crc64update( txt, h64, l64 )
      h_sha.update( txt )
      h_sha1.update( txt )
      h_sha224.update( txt )
      h_sha256.update( txt )
      h_sha384.update( txt )
      h_sha512.update( txt )
      h_ripemd160.update( txt )
      h_whirlpool.update( txt )

  inp.close()

  if only_md5:
    print( h_md5.hexdigest(), "[%s]" % binascii.b2a_base64( h_md5.digest() )[:-1].decode('ascii'), fnm )
  else:
    print( '  crc32    ', '%08x' % (h_crc32 & 0xFFFFFFFF) )
    if with_crc64: print( '  crc64    ', "%08x%08x" % (h64,l64) )
    print( '  md4      ', h_md4.hexdigest() )
    print( '  md5      ', h_md5.hexdigest(), "'%s'" % binascii.b2a_base64( h_md5.digest() )[:-1].decode('ascii') )
    print( '  ripemd160', h_ripemd160.hexdigest() )
    print( '  sha      ', h_sha.hexdigest() )
    print( '  sha1     ', h_sha1.hexdigest(), "'%s'" % binascii.b2a_base64( h_sha1.digest() )[:-1].decode('ascii') )
    print( '  sha224   ', h_sha224.hexdigest() )
    print( '  sha256   ', h_sha256.hexdigest() )
    s = h_sha384.hexdigest(); print( '  sha384   ', s[:64]+"\n", ' '*10, s[64:] )
    s = h_sha512.hexdigest(); print( '  sha512   ', s[:64]+"\n", ' '*10, s[64:] )
    s = h_whirlpool.hexdigest(); print( '  whirlpool', s[:64]+"\n", ' '*10, s[64:] )

p64 = False
md5 = False
for fmm in sys.argv[1:]:
  if fmm=="+64":
    p64 = True
    continue
  if fmm=="md5":
    md5 = True
    continue
  for fnm in glob.glob( fmm ):
    if not os.path.isfile( fnm ):
      continue
    print_chksums( fnm, with_crc64=p64, only_md5=md5 )
