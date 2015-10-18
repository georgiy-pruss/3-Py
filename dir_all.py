copyright = "Copyright (C) 2004,2009 by Georgy Pruss"

# General modules
import os
import sys
import time

# System-dependent
try:
  from win32file import GetCompressedFileSize, GetDiskFreeSpace # GetDiskFreeSpaceEx
except (NameError, ImportError):
  def GetCompressedFileSize( file ):
    return os.stat( file ).st_size # return normal size instead
  def GetDiskFreeSpace( disk ):
    # on Unix it should be written with statvfs( path )
    return (1,512,0,0) # some fake data, zeros for free and total clusters
try:
  from os import startfile
except (NameError, ImportError):
  startfile = None


def loc_format( number ):
  res = ''
  tmp = "%d" % number
  while len(tmp) > 3:
    res = ',' + tmp[-3:] + res
    tmp = tmp[:-3]
  return tmp + res


indent = 0
spaces = 250*'. '


class File:

  def __init__(self,name,size,log_size,mtime,ctime,atime):
    self.name = name
    self.size = size # on disk!
    self.log_size = log_size
    self.mtime = mtime
    self.ctime = ctime
    self.atime = atime

  def calc_size( self ):
    return self.size

  def __str__( self, ind=0 ):
    if self.name == ".": return ""
    return "%s%s\n" % (spaces[:indent],self.name)

  def xml( self ):
    c,m,a = self.ctime, self.mtime, self.atime
    if m==c: m=1
    if a==c: a=1
    elif a==m: a=2
    return ("<f n=\"%s\" d='%d' s='%d' c='%d' m='%d' a='%d' />\n" %
      (self.name.replace("\"","\\\""), self.size, self.log_size, c,m,a))

class Dir(File):

  def __init__( self, name, mtime, ctime, atime ):
    File.__init__( self, name, 0, 0, mtime, ctime, atime )
    self.items = []

  def add_item( self, item ):
    self.items.append( item )

  def calc_size( self ):
    sz = 0
    for it in self.items:
      sz += it.calc_size()
    self.size = sz
    return sz

  def __str__( self ):
    global indent
    dirs = []
    s = "%s%s [%d] %s\n" % (spaces[:indent], self.name, len(self.items)-1, self.path)
    indent += 2
    for it in self.items:
      if isinstance(it,Dir):
        dirs.append(it)
      else:
        s += "%s" % str(it)
    for it in dirs:
      s += "%s" % str(it)
    indent -= 2
    return s

  def xml( self ):
    c,m,a = self.ctime, self.mtime, self.atime
    if m==c: m=1
    if a==c: a=1
    elif a==m: a=2
    s = ("<d n=\"%s\" d='%d' s='%d' c='%d' m='%d' a='%d' i='%d'>\n" %
      (self.name.replace("\"","\\\""),self.size, self.log_size, c,m,a,
      len(self.items)))
    for it in self.items:
      t = "%s" % it.xml()
      #if "\".\"" in t:
      #  t = t.replace("/>","was=\"%s\" />" % self.name.replace("\"","\\\""))
      s += t
    s += "</d>\n"
    return s


def walk_dir( path, dir_name ):

  global vars

  s = os.stat( path )
  mtime = s.st_mtime
  ctime = s.st_ctime
  atime = s.st_ctime
  d = Dir( dir_name, mtime, ctime, atime )
  d.path = path

  try:
    directory = os.listdir( path )
  except WindowsError:
    # ignore errors like no access to 'C:/System Volume Information/*.*'
    vars.dirs += 1
    return d

  BITS = vars.di.cluser_size_bits
  MASK = vars.di.cluser_size_mask

  for name in directory:
    full_name = os.path.join( path, name )
    try:
      s = os.stat( full_name )
    except WindowsError:
      print( "***",full_name )
      continue
    if os.path.isdir( full_name ):
      #tip.show( "%4d %s" % (vars.dirs, full_name) )
      new_d = walk_dir( full_name, name ) # do dirs right away
      d.add_item( new_d )
      d.size += new_d.size
      d.log_size += new_d.log_size
    elif os.path.isfile( full_name ):
      logsz = s.st_size
      try:
        sz = GetCompressedFileSize( full_name )
      except: # pywintypes.error
        sz = logsz
      if sz < 60: # we ignore short files
        sz = 0
      else:
        sz = (sz + BITS) & MASK
      f = File( name, sz, logsz, s.st_mtime, s.st_ctime, s.st_atime )
      d.add_item( f )
      d.size += sz
      d.log_size += logsz
      vars.files += 1
      if sz > 8000000:
        vars.huge_files.append( "%13s %s" % (loc_format(sz), full_name) )

  # Now add dir itself
  sz = len(d.items) * 128 # let's assume 128 bytes per file (but IT CAN BE 512)
  sz = (sz + BITS) & MASK
  f = File( ".", sz, 0, 0, 0, 0 )
  d.add_item( f )
  d.size += sz

  vars.dirs += 1

  return d


class DiskInfo:

  def __init__( self, letter ):
    assert len(letter) == 1 and 'A' <= letter.upper() <= 'Z'
    self.name = letter + ":\\"
    s,b,f,t = GetDiskFreeSpace( self.name )
    self.sectors_per_cluster = s
    self.bytes_per_sector    = b
    self.free_clusters       = f
    self.total_clusters      = t
    self.cluser_size = cs = s*b
    self.free_size   = cs * f
    self.total_size  = cs * t
    self.cluser_size_bits = cs - 1
    self.cluser_size_mask = (2**48-1) ^ (cs - 1)


class Variables:

  def __init__( self ):
    self.dirs  = 0
    self.files = 0
    self.huge_files = []

    if len(sys.argv) == 2:
      a = sys.argv[1]
      if a.endswith( "\\" ) and a[1:3]!=":\\":
        a = a[:-1]
      self.root_dir = dir = a
      if not os.path.exists( dir ):
        print( "Not found: <<%s>>" % dir )
        sys.exit(0)
      if not os.path.isdir( dir ):
        print( "Not directory: <<%s>>" % dir )
        sys.exit(0)
      if dir[1:3]==":\\":
        curdir = dir
      else:
        curdir = os.getcwd()
      assert curdir[1:3]==":\\"
      self.drive = curdir[0]
    else:
      print( "call with dir as argument" )
      sys.exit(0)

    self.root_name = self.root_dir

    self.di = DiskInfo( self.drive )


def log( txt ):
  f = open( "dir_all.log", "at" )
  print( txt, file=f )
  f.close()


vars = Variables()

out = "%s  %s" % (vars.root_dir, time.strftime( "%m%d %H%M" ) )

clstr = vars.di.cluser_size<1000 and ("%3d"%vars.di.cluser_size) or ("%2dK"%(vars.di.cluser_size//1024))
out += "  %s  %7.3f  %7.3f" % (clstr,
  vars.di.total_size/1e9, vars.di.free_size/1e9)

def make_all( vars ):
  # top-level directory
  t = time.clock()
  root = walk_dir( vars.root_dir, vars.root_name )
  vars.took = time.clock()-t

  # these are fast
  root.calc_size()

  return root

root = make_all( vars )

f = open("output.txt","wt",encoding="utf-8")
print( root, file=f ) # root.xml()
f.close()

print( vars.dirs,"dirs,",vars.files,"files,","%.1f seconds" % vars.took )

out += "  %7.3f  %5d %7d" % (root.size/1e9, vars.dirs, vars.files)

fpd = float(vars.files)/vars.dirs
bpf = float(root.size)/vars.files
bpd = float(root.size)/vars.dirs

bpdstr = bpd<100e3 and ("%4.1f"%(bpd/1e3)) or ("%4.0f"%(bpd/1e6))
out += "  %5.1f  %s  %6.0f  %5.1f" % (fpd,bpdstr,bpf/1e3,vars.took)

log( out )

#log( "Huge files (%d)" % len(vars.huge_files) )
#for line in sorted(vars.huge_files):
#  log( line )

# EOF
