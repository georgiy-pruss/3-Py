import sys

try:
  from win32file import GetDiskFreeSpace
except (NameError, ImportError):
  print( "No win32file. See http://sourceforge.net/projects/pywin32/files/" )
  sys.exit(0)

from utils import format_int

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

if len(sys.argv)<2:
  print( "Syntax: disk_info.py disk [disk]..." )
  sys.exit(0)

for d in sys.argv[1:]:
  d = d[:1].upper()
  di = DiskInfo(d)
  l1 = d+": "
  l2 = "   "
  l3 = "   "
  l1 += "Sec sz %5s | " % format_int( di.bytes_per_sector )
  l2 += "Sec/cl %5s | " % format_int( di.sectors_per_cluster )
  l3 += "Cl sz %6s | " % format_int( di.cluser_size )
  l1 += "Free  cl %11s | " % format_int( di.free_clusters )
  l2 += "Occup cl %11s | " % format_int( di.total_clusters - di.free_clusters )
  l3 += "Total cl %11s | " % format_int( di.total_clusters )
  l1 += "Free  sz %17s | " % format_int( di.free_size )
  l2 += "Occup sz %17s | " % format_int( di.total_size - di.free_size )
  l3 += "Total sz %17s | " % format_int( di.total_size )
  l1 += "%7.3f%%" % (100.0*float(di.free_size)/float(di.total_size))
  l2 += "%7.3f%%" % (100.0*float(di.total_size - di.free_size)/float(di.total_size))
  l3 += "%7dM" % ((di.total_size+70000)//2**20)

  print()
  print( l1 )
  print( l2 )
  print( l3 )
