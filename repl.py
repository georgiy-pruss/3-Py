import sys,os,fnmatch


def substitute(s):
  for f,t in (("@V","|"),("@S"," "),("@A","'"),("@N","\x0A"),
              ("@L","<"),("@E","\x1B"),("@Q","\""),("@R","\x0D"),
              ("@G",">"),("@B","\b"),("@C",":"),("@K","\\"),
              ("@M","&"),("@P","%"),("@U","^"),("@T","\t"),("@D","$"),
              ("@@","@")):
    s = s.replace(f,t)
  return s

def process_file(infile,args):
  txt = infile.read()
  replaced = False
  for arg in args:
    p1,p2 = arg.split(":")
    p1 = substitute(p1)
    if p1 in txt:
      replaced = True
      p2 = substitute(p2)
      txt = txt.replace(p1,p2)
  return replaced and txt or None


def process_dir( d, filepattern, subs, recursive=False ):
  for filename in os.listdir("."):
    if os.access(filename,os.F_OK) and fnmatch.fnmatch(filename,filepattern):
      try:
        print( filename, end=" " )
        infile = open( filename, 'rt', encoding="utf-8", errors="replace" )
        res = process_file(infile,subs)
        if res==None:
          print( "-" )
        else:
          outfile = open( filename+"_n", 'wt', encoding="utf-8" )
          print( res, end="", file=outfile )
          outfile.close()
          print( "+" )
      except IOError as e:
        print( "x", e )
      finally:
        infile.close()

if len(sys.argv)<3:
  print( """repl.py filemask from:to [...]
@S = SPC  @V = |  @K = \\  @M = &  @C = :  @T = TAB
@E = ESC  @L = <  @A = '  @P = %  @D = $  @N = NL
@B = BSP  @G = >  @Q = "  @U = ^  @@ = @  @R = CR""" )
# @abcde_g___klmn_pqrstuv____
else:
  files = sys.argv[1]
  subs = sys.argv[2:]
  args_ok = True
  for arg in subs:
    if arg.count(":")!=1:
      print( "Wrong argument:",arg )
      args_ok = False
  if args_ok:
    process_dir( ".", files, subs )

