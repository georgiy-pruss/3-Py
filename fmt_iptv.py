# Read "iptv.m3u8" and write three output files in different formats
# Get it yourself, e.g. wget http://<...ip...>/iptv.m3u8

try:
  def opn( s ): return open( s, "wt", encoding="utf-8" )
  asx = opn( "output.asx" ); dpl = opn( "output.dpl" ); lst = opn( "output.txt" )
  with open( "iptv.m3u8", "rt", encoding="utf-8" ) as f:
    # An entry has format:
    # #EXTINF:0 audio-track=0 group-title="Category" tvg-name="TVName"[ tvg-logo="LName"] ,Name
    # http://91.210.251.170/etc
    def fnd( s, sb, se, p=0 ): # string between delimiters and pointer after all
      pb = s.index(sb,p); pe = s.index(se,pb+len(sb)); return s[pb+len(sb):pe],pe+len(se)
    n = 0 # count of entries, needed for *.dpl
    for l in f: # l -- line, no good guess for another var name
      l = l.strip()
      if l.startswith("#EXTINF:"):
        c,e = fnd( l,"group-title=\"","\"") # category
        _,e = fnd( l,"\"","\"",e ); t = l[e:]
        if "tvg-logo=\"" in t:
          _,e = fnd( l,"tvg-logo=\"","\"",e ); t = l[e:]
        while t.startswith(" ") or t.startswith(",") or t.startswith("."):
          t = t[1:] # skip leading space, comma, dot
        t = c + " | " + t # for output, and for saving for later output
        asx.write( "<entry><title>"+t+"</title>" )
        lst.write( t+"\n" )
      elif l.startswith("http"): # and ignore all other lines btw
        asx.write( "<ref href=\"" + l + "\"/>\n" )
        n += 1
        dpl.write( "%d*file*%s\n%d*title*%s\n%d*played*0\n" % (n,l,n,t,n) )
  asx.close(); dpl.close(); lst.close()
except Exception as e:
  print( e ) # just short report
