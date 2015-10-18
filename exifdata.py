#!/usr/local/bin/python
#
# Creates photodata.txt file or renames files
# Options: -r  -- no recursive
#          ... -- rename pattern:
#            n -- name
#            d -- date YYYYMMDD
#            t -- time HHMMSS
#            i -- iso 80..3200
#            s -- shutter speed ### for 1/###, #s# or ###s for seconds
#            a -- apperture 1.8 2.0 2.2 ... 22
#            f -- focal length, 35 mm equivalent
#            c -- exposure compensation
#
# Exif information decoder
# Written by Thierry Bousch <bousch@topo.math.u-psud.fr>
# Public Domain
#
# $Id: exifdump.py,v 1.13 1999/08/21 14:46:36 bousch Exp $
#
# Since I don't have a copy of the Exif standard, I got most of the
# information from the TIFF/EP draft International Standard:
#
#   ISO/DIS 12234-2
#   Photography - Electronic still picture cameras - Removable Memory
#   Part 2: Image data format - TIFF/EP
#
# You can (and should) get a copy of this document from PIMA's web site;
# their URL is:  http://www.pima.net/it10a.htm
# You'll also find there some documentation on DCF (Digital Camera Format)
# which is based on Exif.
#
# Another must-read is the TIFF 6.0 specification, which can be
# obtained from Adobe's FTP site, at
# ftp://ftp.adobe.com/pub/adobe/devrelations/devtechnotes/pdffiles/tiff6.pdf
#
# Many thanks to Doraneko <doraneko@unioncg.or.jp> for filling the
# holes in the Exif tag list.

import sys,os

EXIF_TAGS = {
  0x100:  "ImageWidth",
  0x101:  "ImageLength",
  0x102:  "BitsPerSample",
  0x103:  "Compression",
  0x106:  "PhotometricInterpretation",
  0x10A:  "FillOrder",
  0x10D:  "DocumentName",
  0x10E:  "ImageDescription",
  0x10F:  "Make",
  0x110:  "Model",
  0x111:  "StripOffsets",
  0x112:  "Orientation",
  0x115:  "SamplesPerPixel",
  0x116:  "RowsPerStrip",
  0x117:  "StripByteCounts",
  0x11A:  "XResolution",
  0x11B:  "YResolution",
  0x11C:  "PlanarConfiguration",
  0x128:  "ResolutionUnit",
  0x12D:  "TransferFunction",
  0x131:  "Software",
  0x132:  "DateTime",
  0x13B:  "Artist",
  0x13E:  "WhitePoint",
  0x13F:  "PrimaryChromaticities",
  0x156:  "TransferRange",
  0x200:  "JPEGProc",
  0x201:  "JPEGInterchangeFormat",
  0x202:  "JPEGInterchangeFormatLength",
  0x211:  "YCbCrCoefficients",
  0x212:  "YCbCrSubSampling",
  0x213:  "YCbCrPositioning",
  0x214:  "ReferenceBlackWhite",
  0x828D: "CFARepeatPatternDim",
  0x828E: "CFAPattern",
  0x828F: "BatteryLevel",
  0x8298: "Copyright",
  0x829A: "ExposureTime",
  0x829D: "FNumber",
  0x83BB: "IPTC/NAA",
  0x8769: "ExifOffset",
  0x8773: "InterColorProfile",
  0x8822: "ExposureProgram",
  0x8824: "SpectralSensitivity",
  0x8825: "GPSInfo",
  0x8827: "ISOSpeedRatings",
  0x8828: "OECF",
  0x9000: "ExifVersion",
  0x9003: "DateTimeOriginal",
  0x9004: "DateTimeDigitized",
  0x9101: "ComponentsConfiguration",
  0x9102: "CompressedBitsPerPixel",
  0x9201: "ShutterSpeedValue",
  0x9202: "ApertureValue",
  0x9203: "BrightnessValue",
  0x9204: "ExposureBiasValue",
  0x9205: "MaxApertureValue",
  0x9206: "SubjectDistance",
  0x9207: "MeteringMode",
  0x9208: "LightSource",
  0x9209: "Flash",
  0x920A: "FocalLength",
  0x927C: "MakerNote",
  0x9286: "UserComment",
  0x9290: "SubSecTime",
  0x9291: "SubSecTimeOriginal",
  0x9292: "SubSecTimeDigitized",
  0xA000: "FlashPixVersion",
  0xA001: "ColorSpace",
  0xA002: "ExifImageWidth",
  0xA003: "ExifImageLength",
  0xA005: "InteroperabilityOffset",
  0xA20B: "FlashEnergy",      # 0x920B in TIFF/EP
  0xA20C: "SpatialFrequencyResponse", # 0x920C    -  -
  0xA20E: "FocalPlaneXResolution",  # 0x920E    -  -
  0xA20F: "FocalPlaneYResolution",  # 0x920F    -  -
  0xA210: "FocalPlaneResolutionUnit", # 0x9210    -  -
  0xA214: "SubjectLocation",    # 0x9214    -  -
  0xA215: "ExposureIndex",    # 0x9215    -  -
  0xA217: "SensingMethod",    # 0x9217    -  -
  0xA300: "FileSource",
  0xA301: "SceneType",
}

INTR_TAGS = {
  0x1:  "InteroperabilityIndex",
  0x2:  "InteroperabilityVersion",
  0x1000: "RelatedImageFileFormat",
  0x1001: "RelatedImageWidth",
  0x1002: "RelatedImageLength",
}

def s2n_motorola(bstr):
  x = 0
  for c in bstr:
    x = (x << 8) | c
  return x

def s2n_intel(bstr):
  x = 0
  y = 0
  for c in bstr:
    x = x | (c << y)
    y = y + 8
  return x


def fracrepr(n,d):
  if n<0:
    return "-"+fracrepr(-n,d)
  if n!=0 and d%n==0: # 1/1 1/5 2/10
    if n==d: return '1'
    return '1/%d' % (d//n)
  if d!=0 and n%d==0: # 0/N N/1 15/5
    return '%d.0' % (n//d)
  if d==10: return '%.1f' % (float(n)/d) # N/10
  if d==100: return '%.2f' % (float(n)/d) # N/100
  assert d!=0
  if (2*n)%d==0 or (5*n)%d==0:
    return '%.1f' % (float(n)/d) # N.5 or N.2 N.4 N.6 N.8
  for i in (6,5,4,3,2): # 12,10,9,8 too
    if n%i==0 and d%i==0:
      n//=i; d//=i
  if 0<n<d and d>=25000 and d%25000==0:
    return (d/n<20 and '1/%.1f' or '1/%.0f') % (d/n)
  if (n,d)==(705,200): return "3.53"
  if (n,d)==(1599,500): return "3.20"
  if (n,d)==(18999,10000): return "1.9"
  if d==65536: return "%.1f" % (float(n)/d) # f-number in Sony MT27i
  return '%d/%d' % (n,d)

class Fraction:

  def __init__(self, num, den):
    self.num = num
    self.den = den

  def __repr__(self):
    """String representation"""
    return fracrepr(self.num,self.den)


class TIFF_file:

  def __init__(self, data):
    self.data = data
    self.endian = data[0]

  def s2n(self, offset, length, signed=0):
    slice = self.data[offset:offset+length]
    if self.endian == ord('I'):
      val = s2n_intel(slice)
    else:
      val = s2n_motorola(slice)
    # Sign extension ?
    if signed:
      msb = 1 << (8*length - 1)
      if val & msb:
        val = val - (msb << 1)
    return val

  def first_IFD(self):
    return self.s2n(4, 4)

  def next_IFD(self, ifd):
    entries = self.s2n(ifd, 2)
    return self.s2n(ifd + 2 + 12 * entries, 4)

  def list_IFDs(self):
    i = self.first_IFD()
    a = []
    while i:
      a.append(i)
      i = self.next_IFD(i)
    return a

  def dump_IFD(self, ifd):
    entries = self.s2n(ifd, 2)
    a = []
    for i in range(entries):
      entry = ifd + 2 + 12*i
      tag = self.s2n(entry, 2)
      type = self.s2n(entry+2, 2)
      if not 1 <= type <= 10:
        continue # not handled
      typelen = [ 1, 1, 2, 4, 8, 1, 1, 2, 4, 8 ] [type-1]
      count = self.s2n(entry+4, 4)
      offset = entry+8
      if count*typelen > 4:
        offset = self.s2n(offset, 4)
      if type == 2:
        # Special case: nul-terminated ASCII string
        values = self.data[offset:offset+count-1]
      else:
        values = []
        signed = (type == 6 or type >= 8)
        for j in range(count):
          if type % 5:
            # Not a fraction
            value_j = self.s2n(offset, typelen, signed)
          else:
            # The type is either 5 or 10
            value_j = Fraction(self.s2n(offset,   4, signed),
                               self.s2n(offset+4, 4, signed))
          values.append(value_j)
          offset = offset + typelen
      # Now "values" is either a string or an array
      a.append((tag,type,values))
    return a


def print_IFD(fields, dict=EXIF_TAGS):
  res = {}
  for (tag,type,values) in fields:
    if tag not in (0x10F,0x110,0x132,0x829A,0x829D,0x8827,0x9003,0x9004,
        0x9202,0x9204,0x9205,0x9209,0x920A,0xA405,0x9102,0x927C):
      continue
    #try:
    #  stag = dict[tag]
    #except:
    #  stag = '0x%04X' % tag
    #stype = ['B',  # BYTE
    #         'A',  # ASCII
    #         'S',  # SHORT
    #         'L',  # LONG
    #         'R',  # RATIONAL
    #         'SB', # SBYTE
    #         'U',  # UNDEFINED
    #         'SS', # SSHORT
    #         'SL', # SLONG
    #         'SR', # SRATIONAL
    #        ] [type-1]
    if   tag==0x10F:  res['make']=values
    elif tag==0x110:  res['model']=values
    elif tag==0x132:  res['dt']=values[:19]
    elif tag==0x829A: res['exp']=values[0]
    elif tag==0x829D: res['f']=values[0]
    elif tag==0x8827: res['iso']=values[0]
    elif tag==0x9003: res['dt1']=values[:19]
    elif tag==0x9004: res['dt2']=values[:19]
    elif tag==0x9202: res['aper?']=values[0]
    elif tag==0x9204: res['bias']=values[0]
    elif tag==0x9205: res['max']=values[0]
    elif tag==0x9209: res['flash']=values[0]
    elif tag==0x920A: res['focal']=values[0]
    elif tag==0xA405: res['fclen']=values[0]
    elif tag==0x9102: res['bpp']=values[0]
    elif tag==0x927C: # maker note
      if 'iso' not in res:
        if len(values)>=187 and values[43]==values[187] and values[42]==values[186]:
          iso = values[42]*256 + values[43]
          if iso in (100,200,220,250,280,320,360,400,450,500,
              560,640,720,800,900,1000,1100,1250,1400,1600,3200):
            res['iso2']=iso
          else:
            res['iso?']=iso
            print( "........ iso",iso, end=" " )
  mindt = b'9999'
  if 'dt' in res and res['dt']<mindt: mindt = res['dt']
  if 'dt1' in res and res['dt1']<mindt: mindt = res['dt1']
  if 'dt2' in res and res['dt2']<mindt: mindt = res['dt2']
  if mindt != b'9999': res['dt']=mindt
  return res

def process_file(ifile):
  """ifile - binary file"""
  data = ifile.read(12)
  if data[0:2]!=b'\xFF\xD8':
    return {}
  if data[2:4]==b'\xFF\xE0' and data[6:10] == b'JFIF':
    length = data[4]*256 + data[5]
    data = ifile.read(length-10) # skip extra
    data = ifile.read(12)
  if data[2:4]!=b'\xFF\xE1' or data[6:10] != b'Exif':
    return {}
  length = data[4]*256 + data[5]
  #print ' Exif header length: %d bytes,' % length,
  data = ifile.read(length-8)
  #print {'I':'Intel', 'M':'Motorola'}[data[0]], 'format'
  T = TIFF_file(data)
  L = T.list_IFDs()
  res = {}
  for i in range(len(L)):
    #print ' IFD %d' % i,
    #if i == 0: print '(main image)',
    #if i == 1: print '(thumbnail)',
    #print 'at offset %d:' % L[i]
    IFD = T.dump_IFD(L[i])
    res.update( print_IFD(IFD) )
    exif_off = 0
    for tag,type,values in IFD:
      if tag == 0x8769:
        exif_off = values[0]
    if exif_off:
      #print ' Exif SubIFD at offset %d:' % exif_off
      IFD = T.dump_IFD(exif_off)
      res.update( print_IFD(IFD) )
      # Recent digital cameras have a little subdirectory
      # here, pointed to by tag 0xA005. Apparently, it's the
      # "Interoperability IFD", defined in Exif 2.1 and DCF.
      intr_off = 0
      for tag,type,values in IFD:
        if tag == 0xA005:
          intr_off = values[0]
      if intr_off:
        #print ' Exif Interoperability SubSubIFD at offset %d:' % intr_off
        IFD = T.dump_IFD(intr_off)
        res.update( print_IFD(IFD, dict=INTR_TAGS) )
  return res

def print_res( filename, res, out ):
  """res - dictionary str->value
  out - text file
  """
  if res['model']==b"NIKON D50" and 'iso2' in res: res['iso'] = res['iso2']
  if 'iso' not in res: res['iso']="?"
  #res['make'][:4],\
  #"("+str(res['focal'])+")",\
  fl = {0:'No',1:'Fired',5:'Fired-', # no return sensed
        16:'Off',32:'NotAvl',7:'Fired+', # return sensed
         9:'Fill',13:'Fill-',15:'Fill+',
        24:'AutoNo',25:'Auto',29:'Auto-',31:'Auto+',89:'RedEye'}
  if 'bpp' not in res: res['bpp']="?" # could use 'Compression' tag
  bpp = str(res['bpp'])
  if bpp.endswith(".0"): bpp=bpp[:-2]
  if '.' in bpp and bpp.endswith('0'): bpp=bpp[:-1]
  if len(bpp)>1 and "/" in bpp:
    nomin,denom = bpp.split("/")
    bpp = "%1.0f" % (float(nomin)/float(denom))
  bias = ('bias' in res) and str(res['bias']) or "0"
  if bias.endswith(".0"): bias=bias[:-2]
  if bias!="0" and bias[0]!="-": bias="+"+bias
  bias=bias.replace("0.66","2/3").replace("0.33","1/3")
  f=str(res['f'])
  if f.endswith(".0"): pass
  elif '.' in f and f.endswith('0'): f=f[:-1]
  output = "%s %5s %4s %-6s %-4s %-6s %1s %4s " % (
    res['dt'][2:].decode("utf-8").replace(":",""),
    res['iso'],f,res['exp'],bias,
    (res['flash'] in fl) and fl[res['flash']] or res['flash'],bpp,res['fclen'])
  print( output, filename, file=out )

def process_dir( d, out, recursive=False, rename='' ):
  good = errors = 0
  for filename in os.listdir("."):
    if os.access(filename,os.F_OK) and filename.lower().endswith(".jpg") and filename[0]!="@":
      try:
        print( filename, end=" " )
        infile = open(filename, 'rb')
        res = process_file(infile)
        infile.close()
        if res:
          if 'dt' not in res or 'make' not in res: # removed this: or 'f' not in res:
            print( "- no dt/make" )
            continue # e.g. FUJI SLP1000SE
          if 'fclen' not in res: res['fclen']='?'
          if 'f' not in res: res['f']='?' # e.g. samsung galaxy samples
          if 'exp' not in res: res['exp']='?'
          if 'flash' not in res: res['flash']='?'
          if rename=="-d":
            dt_tm = res['dt'].decode("utf-8").replace(":","").replace(" ","_")
            os.rename( filename, dt_tm+"_"+filename )
          elif rename=="-i":
            if res['model']==b"NIKON D50" and 'iso2' in res: res['iso'] = res['iso2']
            if 'iso' not in res and 'iso2' in res: res['iso'] = res['iso2']
            if 'iso' not in res and 'iso?' in res: res['iso'] = res['iso?']
            if 'iso' in res:
              sfx = str(res["iso"])
              exp = str(res["exp"])
              if "/" in exp:
                exp1,exp2 = exp.split("/")
                sfx += "_"+exp2
              else:
                if "." in exp:
                  sfx += "_"+exp.replace(".","s")
                else:
                  sfx += "_"+exp+"s"
              nm = filename[:-4]+"_"+sfx+".jpg"
              print( "-->",nm, end=" " )
              os.rename( filename, nm )
          else:
            print_res( filename, res, out )
          if 'iso?' in res:
            errors += 1 # to pause for showing suspicious iso
            print( "?" )
          else:
            print( "+", res['model'].decode("utf-8").lower() )
          good += 1 # could read a file, it has some data, maybe not all
        else:
          print( "-" )
      except IOError:
        print( "- cannot open file" )
        errors += 1
      except Exception as unknown_exception:
        print( ":", unknown_exception )
        errors += 1
  return good,errors
  #for root, dirs, files in os.walk(d, topdown=False):
  #  print "\n"+root+":\n"
  #  for name in files:
  #    if filename.lower().endswith(".jpg") and filename[0]!="@":
  #      print os.path.join(root, name)

def main(args):
  frename=""
  if "-d" in args: frename = "-d"
  if "-i" in args: frename = "-i"
  if frename:
    good,errors = process_dir( ".", None, recursive=True, rename=frename )
    print( "%6d files"%good )
    return

  print("Use -d or -i for renaming files")
  NM,NM2,NM3 = "photodata.txt","photodata_.txt","photodata__.txt"
  if os.access(NM,os.F_OK):
    if os.access(NM2,os.F_OK):
      try: os.rename(NM2,NM3)
      except: pass
    try: os.remove(NM2)
    except: pass
    os.rename(NM,NM2)
  out = open(NM,"wt")
  print( "date   time     iso fnum expos  bias flash  bpp fl  file", file=out )
  good,errors = process_dir( ".", out, recursive=True, rename="" )
  print( "%6d files"%good, file=out )
  out.close()
  input(errors and "errors..." or "all ok")

if __name__ == '__main__':
  main(sys.argv[1:])
