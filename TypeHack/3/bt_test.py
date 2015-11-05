# tests for bt.py                   20120425-050607

from re import search
from time import time,timezone,daylight
from operator import mul,add
from bt import pad,fit,repl,hms,dhms,wdhms,date_data
from os import getcwd,sep

# list .a(x) .fold .n .j .i .f .s .j(s) abs

a = []
a.a( 1 ); assert a == [1]
a.a( 2.0 ); assert a == [1,2.0]
a.a( 3e33 ); assert a == [1,2.0,3e33]
a.a( False ); assert a == [1,2.0,3e33,False]
a.a( "FIVE" ); assert a == [1,2.0,3e33,False,"FIVE"]
a.a( [6,(7,)] ); assert a == [1,2.0,3e33,False,"FIVE",[6,(7,)]]

assert [1,2,3,4,5].fold(add,0) == 15
assert [1,2,3,4,5].fold(mul,1) == 120
assert ['x','y','z'].fold(add,'') == 'xyz'

assert [].n == 0
assert [1].n == 1
assert [1,2,3,4,5].n == 5

assert [].i == []
assert [1.2, 2.9, -3.4].i == [1,2,-3]
assert ["0","-22","  333   "].i == [0,-22,333]

assert [].f == []
assert [1, 2, -3].f == [1.0,2.0,-3.0]
assert ["0","-22","  333e44"].f == [0.0,-22.0,3.33e46]

assert [1,2e2,True].s == ["1","200.0","True"]

assert [1,22,333].j() == "122333"
assert [1,22,333].j("<>") == "1<>22<>333"
assert ["a","b","c"].j() =="abc"
assert ["a","b","c"].j(", ") =="a, b, c"

assert [].abs == [] and [-3].abs == [3]
assert [-3,2,-1,0,-20,30].abs == [3,2,1,0,20,30]

# tuple .fold .n .i .f .s .j(s)

assert (1,2,3,4,5).fold(add,0) == 15
assert (1,2,3,4,5).fold(mul,1) == 120
assert ('x','y','z').fold(add,'') == 'xyz'

assert ().n == 0
assert (1,).n == 1
assert (1,2,3,4,5).n == 5

assert (0.2,-22.9,00333.3300).i == (0,-22,333)
assert ("0","-22","  333   ").i == (0,-22,333)

assert ( 0 , -22 ,   333e44 ).f == (0.0,-22.0,3.33e46)
assert ("0","-22","  333e44").f == (0.0,-22.0,3.33e46)

assert (1,2e2,True).s == ("1","200.0","True")

assert (1,22,333).j() == "122333"
assert (1,22,333).j("..") == "1..22..333"
assert ("a","b","c").j() =="abc"
assert ("a","b","c").j(",") =="a,b,c"

# dict .n .j(s,p) .k .v

assert {}.n == 0
assert {1:2}.n == 1
assert {3:4,5:6}.n == 2

assert {1:2,3:4}.j() in ("1:2,3:4","3:4,1:2")
assert {1:2,3:4}.j("\n") in ("1:2\n3:4","3:4\n1:2")
assert {1:2,3:4}.j(" + ","*") in ("1*2 + 3*4","3*4 + 1*2")
assert {'a':'b'}.j("1","2") == "a2b"

d = {1:'a',2:'b',3:'c',4:'d'}
assert sorted(d.k) == [1,2,3,4]
assert sorted(d.v) == ['a','b','c','d']

# float .deg .i .s .abs .rnd

INF = 1e300*1e300; NAN = INF/INF
assert 57.29577951308232.deg == 1.0
assert 57.29577951308232.i == 57 and -9.9.i == -9
assert 57.29577951308232.s == "57.29577951308232"
assert INF.s == 'inf' and NAN.s == 'nan'
assert (-INF).s == '-inf' and (-NAN).s == 'nan'
assert (-0.0).s == '-0.0'
assert 1.5.abs == (-1.5).abs == 1.5
assert INF.abs == (-INF).abs == INF
assert NAN.abs != (-NAN).abs != NAN # all NANs are different!
assert (-0.0).abs == 0.0

for i in 1000 .r: assert 0.0<=1.0.rnd<1.0
for i in 1000 .r: assert 0.0<=10.0.rnd<10.0
for i in 1000 .r: assert 0.0<=0.001.rnd<0.001

# int .deg .s .f .abs .rnd .x .X .b .r

assert 360 .deg == 6.283185307179586
assert 220 .s == "220"
assert 100 .f == 100.0 and type(100 .f) == float
assert 1 .abs == (-1).abs == 1
assert (-1234567890123456).abs == 1234567890123456

for i in 1000 .r: assert 2 .rnd in (0,1)
for i in 1000 .r: assert 0 <= 9 .rnd < 9
for i in 1000 .r: assert 0 <= 100 .rnd < 100

assert 0 .x == '0' and 0 .X == '0' and 0 .b == '0'
assert 1 .x == '1' and 1 .X == '1' and 1 .b == '1'
assert 255 .x == 'ff' and 255 .X == 'FF' and 255 .b == '11111111'
assert (-10).x == "-a" and (-160).X == "-A0" and (-2560).b == '-101000000000'
assert 0x000A.x == 'a' and 0x000A.X == 'A' and 0x000A.b == '1010'
assert 0xA000.x == 'a000' and 0xA000.X == 'A000' and 0xA000.b == '1010000000000000'
assert 0b1100110010100101.b == '1100110010100101'

assert list(0 .r) == []
assert list(1 .r) == [0]
assert list(2 .r) == [0,1]
assert list(3 .r) == [0,1,2]

# range .l

assert range(0).l == []
assert range(1).l == [0]
assert range(2).l == [0,1]
assert range(3).l == [0,1,2]
assert range(2,8).l == [2,3,4,5,6,7]
assert range(2,14,3).l == [2,5,8,11]

assert 0 .r.l == []
assert 1 .r.l == [0]
assert 2 .r.l == [0,1]
assert 3 .r.l == [0,1,2]

# generator .l

assert (x for x in 5 .r).l == [0,1,2,3,4]
assert (x for x in "abcdef").l == ["a","b","c","d","e","f"]

# object .isa

'x'.isa(str)
(1).isa(int)
1.2.isa(float)
b'x'.isa(bytes)
{1:2}.isa(dict)
[1,2].isa(list)
(1,2).isa(tuple)
10 .r.isa(range)

# bytes .n .b .s

assert b''.n == 0 and b'a'.n == 1 and b'abcdef'.n == 6
assert b'\0\x01\x80\xEE\xFF'.b == b'\0\x01\x80\xEE\xFF' # self
assert '00112233445566778899aabbccdDEeff' == b'00112233445566778899aabbccdDEeff'.s
assert '\0\x01+-*/.^&01abAB\x7F' == b'\0\x01+-*/.^&01abAB\x7F'.s

# bytes .xx .x .X .xor(b)

a = b'0011223344556677-8899aabbccddeeff'.xx
b = b'0123456789abcdef 0123456789abcdef'.xx
c = b'01326754cdfeab98:89baefdc45762310'.xx
assert a.xor(b) == c
assert c.x == '01326754cdfeab9889baefdc45762310'
assert c.X == '01326754CDFEAB9889BAEFDC45762310'

assert b'0101'.xx.xor(b'0011 000_111'.xx) == b'0110 000_111'.xx
assert b'0101000111xyz'.xor(b'0011') != b'0110000111xyz'
assert b'0101000111xyz'.xor(b'\x00\x00\x01\x01') == b'0110000111xyz'
assert b'0101000111xyz'.xor(b'') == b'0101000111xyz'

# str .n .b .xx

assert b''.n == 0 and b'a'.n == 1 and b'abcdef'.n == 6
assert '00112233445566778899aabbcCDdeeff'.b == b'00112233445566778899aabbcCDdeeff'
assert '\0\x01+-*/.^&01abAB\x7F'.b == b'\0\x01+-*/.^&01abAB\x7F' # only 0..127 in str
assert '0123456789abcdef'.xx == b'0123456789abcdef'.xx
a = '0011223344556677 8899aabbccddeeff'.xx
b = '0123456789abcdef 0123456789abcdef'.xx
c = '01326754cdfeab98 89baefdc45762310'.xx
assert a.xor(b) == c # bytes

# str .pad(n,c=' ') .fit(n,c=' ')

assert ''.pad(3) == ''.fit(3) == '   '
assert ''.pad(3,'x') == ''.fit(3,'x') == 'xxx'

assert ''.pad( 6,'abc') == ''.fit( 6,'abc') == 'abcabc'
assert ''.pad( 5,'abc') == ''.fit( 5,'abc') == 'abcab'
assert ''.pad( 4,'abc') == ''.fit( 4,'abc') == 'abca'
assert ''.pad( 3,'abc') == ''.fit( 3,'abc') == 'abc'
assert ''.pad( 2,'abc') == ''.fit( 2,'abc') == 'ab'
assert ''.pad( 1,'abc') == ''.fit( 1,'abc') == 'a'
assert ''.pad( 0,'abc') == ''.fit( 0,'abc') == ''
assert ''.pad(-1,'abc') == ''.fit(-1,'abc') == 'c'
assert ''.pad(-2,'abc') == ''.fit(-2,'abc') == 'bc'
assert ''.pad(-3,'abc') == ''.fit(-3,'abc') == 'abc'
assert ''.pad(-4,'abc') == ''.fit(-4,'abc') == 'cabc'
assert ''.pad(-5,'abc') == ''.fit(-5,'abc') == 'bcabc'
assert ''.pad(-6,'abc') == ''.fit(-6,'abc') == 'abcabc'

assert '123'.pad( 7,'abc') == '123abca'
assert '123'.pad( 6,'abc') == '123abc'
assert '123'.pad( 5,'abc') == '123ab'
assert '123'.pad( 4,'abc') == '123a'
assert '123'.pad( 3,'abc') == '123'
assert '123'.pad( 2,'abc') == '123'
assert '123'.pad( 1,'abc') == '123'
assert '123'.pad( 0,'abc') == '123'
assert '123'.pad(-1,'abc') == '123'
assert '123'.pad(-2,'abc') == '123'
assert '123'.pad(-3,'abc') == '123'
assert '123'.pad(-4,'abc') == 'c123'
assert '123'.pad(-5,'abc') == 'bc123'
assert '123'.pad(-6,'abc') == 'abc123'
assert '123'.pad(-7,'abc') == 'cabc123'

assert '123'.fit( 7,'abc') == '123abca'
assert '123'.fit( 6,'abc') == '123abc'
assert '123'.fit( 5,'abc') == '123ab'
assert '123'.fit( 4,'abc') == '123a'
assert '123'.fit( 3,'abc') == '123'
assert '123'.fit( 2,'abc') == '12'
assert '123'.fit( 1,'abc') == '1'
assert '123'.fit( 0,'abc') == ''
assert '123'.fit(-1,'abc') == '3'
assert '123'.fit(-2,'abc') == '23'
assert '123'.fit(-3,'abc') == '123'
assert '123'.fit(-4,'abc') == 'c123'
assert '123'.fit(-5,'abc') == 'bc123'
assert '123'.fit(-6,'abc') == 'abc123'
assert '123'.fit(-7,'abc') == 'cabc123'

# str .n .s(x) .e(x) .l .u .p .k .ints

assert ''.n == 0 and 'a'.n == 1 and 'abcdef'.n == 6
assert 'abcdef'.s('a') and 'abcdef'.s('abc') and not 'abcdef'.s('x')
assert 'abcdef'.e('f') and 'abcdef'.e('def') and not 'abcdef'.s('x')
assert "ABcd".l == "abcd"
assert "ABcd".u == "ABCD"
assert "\u00DF".u == "\u00DF".l == "\u00DF" # &szlig; german s-zet
assert " \tABC\n\t ".p == "ABC"                   # striP = Prettify
assert "abc 2\t##\n\tG".k == ['abc','2','##','G'] # breaK
assert "x1-2+3=000 -099 111_222.333:444x".ints == [1,-2,3,0,-99,111,222,333,444]

# str .c(x) .f(x) .r(*xy) .m(x)

assert "".c("x") == 0 and "abcd".c("x") == 0
assert "abcdef".c("cd") == 1 and "abcdcdef".c("cd") == 2
assert "".f("x") == -1 and "abcd".f("x") == -1
assert "abcdef".f("cd") == 2 and "abcdcdef".f("cd") == 2
assert "abcd".r("xy","z","bc","^","^d","i-end","ai","start") == "start-end"
assert "abcd".m("^a") and not "abcd".m("a$")

# match .i .s

m = "abcdefghicxgm".m("c.*g") # greedy
assert m.i == 2 and m.s == "cdefghicxg"
m = "abcdefghicxgm".m("c.*?g")
assert m.i == 2 and m.s == "cdefg"
m = "abcdefghicxgm".m("c(.)g")
assert m.i == 9 and m.s == "cxg"
assert m.group(1) == 'x'
m = "abcdefghicxgm".m("c[~]g")
assert not m

# str .mm(x) .sub(x,y)

assert "abcdcdab".mm("c.*d") == ["cdcd"]
assert "abcdcdab".mm("c.*?d") == ["cd","cd"]
assert "abcd".mm(".") == ["a","b","c","d"]
assert "abcd".mm("..") == ["ab","cd"]
assert "1 23 456 7890".mm("\\d+") == ["1","23","456","7890"]

assert "abcd".sub("[bd]","<>") == "a<>c<>"
assert "0A FF".sub("[0-9A-Fa-f]+",lambda m:str(int(m.group(),16))) == "10 255"

# FILEs/DIRs

# str ._n _f _r _w _x _d _t _dir _del() _data[=x]

fname,data = "a_b_c_1.x_x",b'1234567'

t1 = ''.t-0.1 # can't use plain ''.t b/c it can be truncated
fname._data = data # save
t2 = ''.t+0.1
assert "."._d
assert fname._f
assert fname._r
assert fname._w
assert fname._x
assert not fname._d
assert fname._n == data.n
assert t1 <= fname._t <= t2
assert fname in "."._dir
assert fname._data == data # load
fname._del()
assert not fname._f

# str ._lines _o([m,e]) _rd([m,e]) _wr(t[m,e])

lines = ["abc\n","\n","defgh\n"]
text = lines.j()
last = "last line\n"

assert fname._wr(text) # not tested: bin/text modes, encodings
assert fname._rd() == text
assert fname._lines == lines
for i,line in enumerate(fname._o()): assert line == lines[i]
assert fname._wr(last,"at")
assert fname._rd() == text+last
fname._del()
assert not fname._f

# str ._abspath _dn _bn

cwd = getcwd()
assert fname._dn == ""
assert fname._bn == fname
assert fname._abspath == cwd+sep+fname # no need to create file
assert fname._abspath._dn == cwd
assert fname._abspath._bn == fname
assert ""._abspath == "."._abspath == cwd

# TIME

TZ = -timezone                # local TZ in seconds, west -, east +     | 7200
DST = daylight and 3600 or 0  # DST 0 or 3600                           | 3600

# int .j

assert 0 .j == 2440587.5
assert (12*3600).j == 2440588
assert 1334964375 .j == 2456038.4765625
assert (-62135769600).j == 1721423.5 # January 1 of year 1

# float .j

assert 0.1.j     == 2440587.5000011576
assert 0.01.j    == 2440587.5000001159
assert 0.001.j   == 2440587.5000000116
assert 0.0001.j  == 2440587.5000000011
assert 0.00001.j == 2440587.5

assert 1334964375.12345.j == 2456038.4765639286
assert 1334964375.12346.j == 2456038.4765639290

# int .t

assert 0 .t == -210866760000 # 0 JD == -211 Gsec == Jan.1 4713 BCE Julian
assert 2440588 .t == 12*3600
assert 2456038 .t == 1334923200

# float .t

assert 2440587.5.t == 0
assert 2456038.1.t         == 1334931840.0000080
assert 2456038.01.t        == 1334924063.9999807
assert 2456038.001.t       == 1334923286.4000142
assert 2456038.0001.t      == 1334923208.6399853
assert 2456038.00001.t     == 1334923200.8640065
assert 2456038.000001.t    == 1334923200.0863805
assert 2456038.0000001.t   == 1334923200.0086500
assert 2456038.00000001.t  == 1334923200.0008450
assert 2456038.000000001.t == 1334923200.0000806
assert 2456038.0.t         == 1334923200

assert 2456038.4765625.t == 1334964375 # some 1/128 fractions of day (675s)

# list .t (ZT)

assert time() <= [].t <= time()

assert [2012,4,16,0,0].t      == 1334512800+TZ+DST  # local time!
assert [2012,4,16,0,0].t      == 1334527200-TZ+DST  # local (or this???)
assert [2012,4,16,0,0].t      == 1334512800+TZ+DST  # local
assert [2012,4,16,0,0,0].t    == 1334512800+TZ+DST  # local
assert [2012,4,16,15,41,23].t == 1334569283+TZ+DST  # local
assert [2012,4,21, 2,26,15].t == 1334953575+TZ+DST  # local

assert [1970,1,1, 0,0,0, 0].t   ==      0  # 1970.1.1 0:00
assert [1970,1,1, 0,0,0, 0,0].t ==      0  # 1970.1.1 0:00
assert [1970,1,2, 0,0,0, 0,0].t ==  86400  # 1970.1.2 0:00
assert [1970,1,2, 1,0,0, 0,0].t ==  90000  # 1970.1.2 1:00
assert [1970,1,2, 2,0,0, 1,0].t ==  90000  # 1970.1.2 2:00 W1:00
assert [1970,1,2, 2,0,0, 0,1].t ==  90000  # 1970.1.1 2:00 W0 DST

assert [1971,1,1, 0,0,0, 0].t == 31536000  # one year, 365 days in seconds

assert [2012,4,16,15,41,23, 3].t       == 1334580083.0  # w/o dst
assert [2012,4,16,15,41,23, 2,1].t     == 1334580083.0  # w/dst
assert [2012,4,16,15,41,23, 2,1,9].t   == 1334580083.0  # wd ignored
assert [2012,4,16,15,41,23, 2,1,9,9].t == 1334580083.0  # wd yd ignored
assert [2012,4,16,15,41,23, 300].t     == 1334580083.0  # +3:00
assert [2012,4,16,15,41,23, 10800].t   == 1334580083.0  # +10800sec
assert [2012,4,16,15,41,23, 200,100].t == 1334580083.0  # +2:00, +1:00dst
assert [2012,4,16,15,41,23, 7200,3600].t==1334580083.0  # seconds

assert [2012,4,16,15,41.5].t == 1334569290.0+TZ+DST         # fraction of minutes
assert [2012,4,16,15,41,23.125].t == 1334569283.125+TZ+DST  # fraction of seconds
assert [2012,4,16,15,41.5,0, 2,1].t == 1334580090.0         # fraction of minutes
assert [2012,4,16,15,41,23.125, 2,1].t == 1334580083.125    # fraction of seconds

assert [1966,1,1, 0,0,0, 0].t == -4*365.25*24*3600
assert [1930,1,1, 0,0,0, 0].t == -40*365.25*24*3600
assert [1890,1,1, 0,0,0, 0].t == -(80*365.25-1)*24*3600
assert [1790,1,1, 0,0,0, 0].t == -(180*365.25-2)*24*3600
assert [1690,1,1, 0,0,0, 0].t == -(280*365.25-3)*24*3600
assert [1590,1,1, 0,0,0, 0].t == -(380*365.25-3)*24*3600 # -11,991,628,800
assert [1582,10,15, 0,0,0, 0].t == -12219292800.0        # 15 oct 1582 FR
assert [1582,10, 4, 0,0,0, 0].t == -12219292800.0-86400  #  4 oct 1582 TH

assert [1,1,1, 0,0,0, 0].t == -62135769600 # 1 january of year 1

assert [2070,1,1, 0,0,0, 0].t == (100*365.25)*24*3600
assert [2170,1,1, 0,0,0, 0].t == (200*365.25-1)*24*3600
assert [2270,1,1, 0,0,0, 0].t == (300*365.25-2)*24*3600
assert [2370,1,1, 0,0,0, 0].t == (400*365.25-3)*24*3600
assert [2470,1,1, 0,0,0, 0].t == (500*365.25-3)*24*3600 # 15,778,540,800

assert [1582,10, 4, 0,0,0, 0].t.j == 2299159.5 #  4 oct 1582 0:00 -- last day of JC
assert [1582,10,15, 0,0,0, 0].t.j == 2299160.5 # 15 oct 1582 0:00 -- 1st day of GC
assert [2470, 1, 1, 0,0,0, 0].t.j == 2623209.5

# list .t (CT)

assert [0,0,0].t == -50716800

assert [587,0,0].t == 0
assert [587,3600,1].t == 0
assert [587,36000,10].t == 0
assert [587,36000,9,1].t == 0
assert [587,-3600,-1].t == 0
assert [586,82800,-1].t == 0
assert [586,50400,-10].t == 0
assert [586,50400,-11,1].t == 0

assert [588,0,0].t == 86400
assert [588,3600,0].t == 90000
assert [588,7200,1].t == 90000
assert [588,7200,0,1].t == 90000

assert [587+1000,0,0].t == 1000*86400  # 1k days
assert [587,+100000000,0].t == 100000000 # 100M secs

assert [16033,56483].t == 1334569283+TZ+DST  # [2012,4,16].d==16033
assert [16033,56483,+3].t == 1334580083      # [ 15,41,23].e==56483
assert [16033,56483,+3,0].t == 1334580083
assert [16033,56483,+2,1].t == 1334580083
assert [16033,56483,+300].t == 1334580083

# tuple .t (CT,ZT)

assert time() <= ().t <= time()

assert (587,0,0).t == 0
assert (16033,56483).t == 1334569283+TZ+DST
assert (16033,56483,+3).t == 1334580083
assert (16033,56483,+3,0).t == 1334580083
assert (2012,4,16,00,00).t == 1334512800.0+TZ+DST
assert (2012,4,16,15,41,23).t == 1334569283.0+TZ+DST
assert (2012,4,16,15,41,23,+3).t == 1334580083.0
assert (2012,4,16,15,41,23,+2,1).t == 1334580083.0
assert (2012,4,16,15,41,23,+2,1,0).t == 1334580083.0
assert (2012,4,16,15,41,23,+2,1,0,0).t == 1334580083.0

# list .z(...|True|[tz[,dst]]) .c(True|[tz[,dst]])
# ... z(...) c(...)
# .................

# list .d .wd .yd

assert [].d == (''.t.z()[:3]).d        # current dn
assert [].d.ymd == tuple(''.t.z()[:3]) # current y m d

assert [   1, 1, 1].d == -718577
assert [1582,10, 4].d == -140841
assert [1582,10,15].d == -140840
assert [1694, 8, 9].d ==  -99999
assert [1858,11,17].d ==  -40000 # start of MJD
assert [1878, 9, 5].d ==  -32768
assert [1965, 8, 5].d ==   -1023
assert [1968, 5,24].d ==       0 # Fr (tjd+5)%7
assert [1968, 5,25].d ==       1 # Sa
assert [1970, 1, 0].d ==     586 # zeros can be too
assert [1970, 1, 1].d ==     587
assert [1985, 4,30].d ==    6185
assert [1995,10, 9].d ==    9999
assert [2012, 4,16].d ==   16033
assert [2013, 4, 1].d ==   16383
assert [2023, 2,24].d ==   19999
assert [2038, 1,18].d ==   25441
assert [2058, 2, 8].d ==   32767
assert [2147,10,28].d ==   65535
assert [2242, 3, 8].d ==   99999

assert [   1, 1, 1].wd == 6
assert [1582,10, 4].wd == 4
assert [1582,10,15].wd == 5
assert [1968, 5,24].wd == 5
assert [1968, 5,25].wd == 6
assert [1969,12,31].wd == 3
assert [1970, 1, 1].wd == 4
assert [1985, 4,30].wd == 2
assert [1995,10, 9].wd == 1
assert [2012, 4,15].wd == 0
assert [2012, 4,16].wd == 1

assert [   1, 1, 1].yd == 1
assert [   1,12,31].yd == 365
assert [1970, 1, 1].yd == 1
assert [1970, 1, 2].yd == 2
assert [1970, 2, 1].yd == 32
assert [1970,12,31].yd == 365
assert [1980,12,31].yd == 366
assert [2000,12,31].yd == 366
assert [2100,12,31].yd == 365 # not leap
assert [2200,12,31].yd == 365 # not leap
assert [2300,12,31].yd == 365 # not leap
assert [2400,12,31].yd == 366
assert [1965, 8, 5].yd == 217
assert [1965, 1, 0].yd == 0

# list .e (HMS,DHMS,WDHMS)

assert [23,59,59].e == 24*60*60-1
assert [0,0,1].e == 1
assert [0,1,0].e == 60
assert [1,0,0].e == 3600
assert [1,0,0,0].e == 86400
assert [1,0,0,0,0].e == 604800
assert [52,1,5,49,12].e == 31556952 # Gregorean year, 365.2425 days
assert [52,1,5,48,45.445].e == 31556925.445 # seconds in 1 tropical year

# tuple .d .wd .yd .e

assert (   1, 1, 1).d == -718577
assert (1582,10,15).d == -140840
assert (1968, 5,24).d ==       0
assert (1995,10, 9).d ==    9999
assert (2012, 4,16).d ==   16033
assert (2642, 3, 8).d ==  246096

assert (   1, 1, 1).wd == 6
assert (1582,10, 4).wd == 4
assert (1582,10,15).wd == 5
assert (1968, 5,24).wd == 5
assert (1968, 5,25).wd == 6
assert (1969,12,31).wd == 3
assert (1970, 1, 1).wd == 4
assert (1985, 4,30).wd == 2
assert (1995,10, 9).wd == 1
assert (2012, 4,15).wd == 0
assert (2012, 4,16).wd == 1

assert (   1, 1, 1).yd == 1
assert (   1,12,31).yd == 365
assert (1970, 1, 1).yd == 1
assert (1970, 1, 2).yd == 2
assert (1970, 2, 1).yd == 32
assert (1970,12,31).yd == 365
assert (1980,12,31).yd == 366
assert (2000,12,31).yd == 366
assert (2100,12,31).yd == 365
assert (1965, 8, 5).yd == 217

assert (23,59,59).e == 24*60*60-1
assert (0,0,1).e == 1
assert (0,1,0).e == 60
assert (1,0,0).e == 3600
assert (1,0,0,0).e == 86400
assert (1,0,0,0,0).e == 604800
assert (52,1,5,49,12).e == 31556952
assert (52,1,5,48,45.445).e == 31556925.445

# int .ymd .wd

assert (-718577).ymd == (   1, 1, 1)
assert (-140841).ymd == (1582,10, 4)
assert (-140840).ymd == (1582,10,15)
assert  (-99999).ymd == (1694, 8, 9)
assert  (-32768).ymd == (1878, 9, 5)
assert   (-1023).ymd == (1965, 8, 5)
assert        0 .ymd == (1968, 5,24) and     0 .wd == 5
assert        1 .ymd == (1968, 5,25) and     1 .wd == 6
assert      586 .ymd == (1969,12,31) and   586 .wd == 3
assert      587 .ymd == (1970, 1, 1) and   587 .wd == 4
assert     6185 .ymd == (1985, 4,30) and  6185 .wd == 2
assert     9999 .ymd == (1995,10, 9) and  9999 .wd == 1
assert    16032 .ymd == (2012, 4,15) and 16032 .wd == 0  # easter
assert    16033 .ymd == (2012, 4,16) and 16033 .wd == 1
assert    16383 .ymd == (2013, 4, 1)
assert    19999 .ymd == (2023, 2,24)
assert    25441 .ymd == (2038, 1,18)
assert    32767 .ymd == (2058, 2, 8)
assert    65535 .ymd == (2147,10,28)
assert    99999 .ymd == (2242, 3, 8)

for i in range(-20000,20000,3): # (-140840,150001):
  assert i.ymd.d == i

# int .yd

assert (-718577).yd == 1
assert      587 .yd == 1
assert      586 .yd == 365

# int .hms .dhms .wdhms

assert 0 .hms == (0,0,0)
assert (24*60*60-1).hms ==    (23,59,59)
assert (24*60*60+1).hms ==      (24,0,1)
assert (24*60*60+1).dhms ==    (1,0,0,1)
assert (24*60*60+1).wdhms == (0,1,0,0,1)
assert (1000*24*60*60-1).dhms == (999,23,59,59)
assert (100*7*24*60*60-1).wdhms == (99,6,23,59,59)

# float .hms .dhms .wdhms

assert (0.0000000000000000000000123).hms == (0,0,0.123e-22)
assert (24*60*60-1+0.11773681640625).hms == (23,59,59.11773681640625)
assert (24*60*60+1.125).hms ==      (24, 0, 1.125)
assert (24*60*60+1.25).dhms ==    (1, 0, 0, 1.25)
assert (24*60*60+1.5).wdhms == (0, 1, 0, 0, 1.5)

# str .t

assert time() <= ''.t <= time()

assert '2012 4 16 15 41 23'.k.i.t  == 1334569283+TZ+DST
assert '2012 4 16 15 41 23'.ints.t == 1334569283+TZ+DST
assert '2012=4=16 15=41=23'.ints.t == 1334569283+TZ+DST
assert '2012 4 16 15 41 23'.t      == 1334569283+TZ+DST # == ints.t
assert '2012*4*16 15*41*23'.t      == 1334569283+TZ+DST
assert '2012_4_16_15_41_23_0'.t    == 1334590883
assert '2012 4 16 15 41 23 +3'.t   == 1334580083
assert '2012 4 16 15 41 23 +2 1'.t == 1334580083
assert '2012.4.16@15:41:23 +2 1'.t == 1334580083

assert 'date 2012-04-16 and time 15:41:23'.ints.abs.t == 1334580083.0
assert 'date 2012-4-16 and time 15:41:23'.t == 1334580083.0

# str .d

assert ''.d == (''.t.z()[:3]).d    # current dn

assert "1968:05:24".d ==     0
assert " 1970 1 1 ".d ==   587
assert "y1985m4d30".d ==  6185
assert "1995~10~9" .d ==  9999
assert "2012,4,16" .d == 16033
assert "2038 1 18 ".d == 25441
assert "2058.2.8  ".d == 32767
assert "2147/10/28".d == 65535
assert "2242-3-8  ".d == 99999

# int .c([tz[dst]]) (tz = ... - keep current tz, but give dst)

t = ''.t.i; H=3600; D=86400
assert t.c(0,0)    == (t//D+587,t%D,0,0)
assert t.c(0)      == (t//D+587,t%D,0,0)
assert t.c(1)      == ((t+H)//D+587,(t+H)%D,H,0)
assert t.c(1,0)    == ((t+H)//D+587,(t+H)%D,H,0)
assert t.c(1,1)    == ((t+2*H)//D+587,(t+2*H)%D,H,H)
assert t.c(2)      == ((t+2*H)//D+587,(t+2*H)%D,2*H,0)
assert t.c(2,0)    == ((t+2*H)//D+587,(t+2*H)%D,2*H,0)
assert t.c(2,1)    == ((t+3*H)//D+587,(t+3*H)%D,2*H,H)
assert t.c(2,+100) == ((t+3*H)//D+587,(t+3*H)%D,2*H,H)
assert t.c(9)      == ((t+9*H)//D+587,(t+9*H)%D,9*H,0)
assert t.c(-8)     == ((t-8*H)//D+587,(t-8*H)%D,-8*H,0)
assert t.c(-8,1)   == ((t-7*H)//D+587,(t-7*H)%D,-8*H,H)
assert t.c(-800,1) == ((t-7*H)//D+587,(t-7*H)%D,-8*H,H)
assert t.c()       == ((t+TZ+DST)//D+587,(t+TZ+DST)%D,TZ,DST)
assert t.c(...)    == ((t+TZ)//D+587,(t+TZ)%D,TZ,0)
assert t.c(...,0)  == ((t+TZ)//D+587,(t+TZ)%D,TZ,0)
assert t.c(...,1)  == ((t+TZ+H)//D+587,(t+TZ+H)%D,TZ,H)

t =  0;               assert t.c(0) == (t//D+587,t%D,0,0) # Python has right //!
t = -1000;            assert t.c(0) == (t//D+587,t%D,0,0)
t = -86400*587;       assert t.c(0) == (t//D+587,t%D,0,0)
t = -86400*587-10000; assert t.c(0) == (t//D+587,t%D,0,0)
t = -86400*588;       assert t.c(0) == (t//D+587,t%D,0,0)
t = -86400*588-80000; assert t.c(0) == (t//D+587,t%D,0,0)
t = -100000000;       assert t.c(0) == (t//D+587,t%D,0,0)
t = -1000000000;      assert t.c(0) == (t//D+587,t%D,0,0)
t = -10000000000;     assert t.c(0) == (t//D+587,t%D,0,0)
t = -50000000000;     assert t.c(0) == (t//D+587,t%D,0,0)

# float .c([tz[dst]])

t = ''.t.i+0.3125 # float
assert t.c(0,0)    == (t//D+587,t%D,0,0)
assert t.c(0)      == (t//D+587,t%D,0,0)
assert t.c(1)      == ((t+H)//D+587,(t+H)%D,H,0)
assert t.c(-8,1)   == ((t-7*H)//D+587,(t-7*H)%D,-8*H,H)
assert t.c()       == ((t+TZ+DST)//D+587,(t+TZ+DST)%D,TZ,DST)
assert t.c(...)    == ((t+TZ)//D+587,(t+TZ)%D,TZ,0)
assert t.c(...,0)  == ((t+TZ)//D+587,(t+TZ)%D,TZ,0)
assert t.c(...,1)  == ((t+TZ+H)//D+587,(t+TZ+H)%D,TZ,H)
t = +10000000000.125; assert t.c(0) == (t//D+587,t%D,0,0)
t =  0.0;             assert t.c(0) == (t//D+587,t%D,0,0)
t = -10000000000.125; assert t.c(0) == (t//D+587,t%D,0,0)

# int .z(~)                       add tests for other args TODO

assert 0 .z(0) == [1970,1,1, 0,0,0, 0,0]
assert 1334580083 .z() == [2012,4,16,15,41,23,TZ,DST]
assert 1334964375 .z() == [2012,4,21, 2,26,15,TZ,DST]
assert (2**31).z(0) == [2038,1,19,  3,14, 8, 0,0]
assert (2**32).z(0) == [2106,2, 7,  6,28,16, 0,0]
assert (2**33).z(0) == [2242,3,16, 12,56,32, 0,0]

# float .z(~)                     add tests DODO

assert 1334580083.5 .z() == [2012,4,16,15,41,23.5,TZ,DST]
assert 1334964375.25 .z() == [2012,4,21, 2,26,15.25,TZ,DST]





# list .z(~) .c(~)             TODO
# tuple .z(~) .c(~)             TODO
# ....
(587,0,0,0).z() == [1970,1,1, 0,0,0, 0,0]  # must be TZ
(587,0,0,0).z(0) == [1970,1,1, 0,0,0, 0,0]
(587,0,0,0).z(True) == [1970,1,1, 0,0,0, 0,0]
(587,0,0,0).z(...) == [1970,1,1, 0,0,0, 0,0]

(1970,1,1, 0,0,0, 0,0).z(0) == [1970,1,1, 0,0,0, 0,0]

(587,0,0,0).c() == (587,0,0,0)
(587,0,0,0).c(0) == (587,0,0,0)
(587,0,0,0).c(True) == (587,0,0,0)
(587,0,0,0).c(...) == (587,0,0,0)

(1970,1,1, 0,0,0, 0,0).c() == (587,0,0,0)


# str .ft([x])
# x can be z ~ DONE, t z c s TODO
# ....

t = (1969,2,3,4,5,6, +3,0, 1,-1); u = (2169,12,31,22,33,44, -9.5,1, 6,-1)
# AaBbDdEeHhMmnOoPpSsTtwYyZz; n - calculated now! XXX
assert "".ft(t) == "$e, $d $o $Y $T $Z".ft(t)
assert "".ft(u) == "$e, $d $o $Y $T $Z".ft(u)
assert "$D $T".ft(t) == "$Y.$m.$d $H:$M:$S".ft(t) == "1969.02.03 04:05:06"
assert "$D $T".ft(u) == "$Y.$m.$d $H:$M:$S".ft(u) == "2169.12.31 22:33:44"
assert "$A $a $B $b".ft(t) == "$E $e $O $o".ft(t)
assert "$A $a $B $b".ft(u) == "$E $e $O $o".ft(u)
assert "$e $E $o $O $P $p".ft(t) == "Mon Monday Feb February  AM"
assert "$e $E $o $O $P $p".ft(u) == "Sat Saturday Dec December DST PM"

date_data["A"] = "Vos Pon Vto Sre Che Pia Sub".k  # change values for AaBbPpDT
date_data["a"] = "0d 1d 2d 3d 4d 5d 6d".k
date_data["B"] = "One Two Three Four Five Six Seven Eight Nine Ten 11en 12ve".k
date_data["b"] = "1m 2m 3m 4m 5m 6m 7m 8m 9m 10m 11m 12m".k
date_data["p"] = ("a.m.","p.m."); date_data["P"] = (";;","st")
date_data["D"] = "$d-$m-$Y"; date_data["T"] = "$hH$M'$S$p"

assert "$D $T".ft(t) == "$d-$m-$Y $hH$M'$S$p".ft(t) == "03-02-1969 04H05'06a.m."
assert "$D $T".ft(u) == "$d-$m-$Y $hH$M'$S$p".ft(u) == "31-12-2169 10H33'44p.m."
assert "$A $a $B $b".ft(t) != "$E $e $O $o".ft(t)
assert "$A $a $B $b".ft(u) != "$E $e $O $o".ft(u)
assert "$e $E $o $O".ft(t) == "Mon Monday Feb February"
assert "$e $E $o $O".ft(u) == "Sat Saturday Dec December"
assert "$a $A $b $B $P $p".ft(t) == "1d Pon 2m Two ;; a.m."
assert "$a $A $b $B $P $p".ft(u) == "6d Sub 12m 12ve st p.m."

assert "$d $H $h $M $m $n".ft(t) == "03 04 04 05 02 034" # n XXX
assert "$S $s $t $w $Y $y $Z $z".ft(t) == "06 $ 000 1 1969 69 +0300 +03:00"
assert "$d $H $h $M $m $n".ft(u) == "31 22 10 33 12 365" # n XXX
assert "$S $s $t $w $Y $y $Z $z".ft(u) == "44 $ 000 6 2169 69 -0930 -09:30"

assert "$29,$ss5%,$$sD$x%%$$$s100%%$$".ft() == "$29,$s5%,$$D$x%%$$$100%%$$"

output = """
1968/01/01 12AM=00:20:30.000 -1200 -12:00 001 --- 0 0d|1m|Vos|One
1969/02/02 01AM=01:21:31.010 -1100 -11:00 033 DST 1 1d|2m|Pon|Two
1970/03/03 02AM=02:22:32.020 -1000 -10:00 062 --- 2 2d|3m|Vto|Three
1971/04/04 03AM=03:23:33.030 -0900 -09:00 094 DST 3 3d|4m|Sre|Four
1972/05/05 04AM=04:24:34.040 -0800 -08:00 126 --- 4 4d|5m|Che|Five
1973/06/06 05AM=05:25:35.050 -0700 -07:00 157 DST 5 5d|6m|Pia|Six
1974/07/07 06AM=06:26:36.060 -0600 -06:00 188 --- 6 6d|7m|Sub|Seven
1975/08/08 07AM=07:27:37.070 -0500 -05:00 220 DST 0 0d|8m|Vos|Eight
1976/09/09 08AM=08:28:38.080 -0400 -04:00 253 --- 1 1d|9m|Pon|Nine
1977/10/10 09AM=09:29:39.090 -0300 -03:00 283 DST 2 2d|10m|Vto|Ten
1978/11/11 10AM=10:30:40.100 -0200 -02:00 315 --- 3 3d|11m|Sre|11en
1979/12/12 11AM=11:31:41.110 -0100 -01:00 346 DST 4 4d|12m|Che|12ve
1980/01/13 12PM=12:32:42.120 +0000 +00:00 013 --- 5 5d|1m|Pia|One
1981/02/14 01PM=13:33:43.130 +0100 +01:00 045 DST 6 6d|2m|Sub|Two
1982/03/15 02PM=14:34:44.140 +0200 +02:00 074 --- 0 0d|3m|Vos|Three
1983/04/16 03PM=15:35:45.150 +0300 +03:00 106 DST 1 1d|4m|Pon|Four
1984/05/17 04PM=16:36:46.160 +0400 +04:00 138 --- 2 2d|5m|Vto|Five
1985/06/18 05PM=17:37:47.170 +0500 +05:00 169 DST 3 3d|6m|Sre|Six
1986/07/19 06PM=18:38:48.180 +0600 +06:00 200 --- 4 4d|7m|Che|Seven
1987/08/20 07PM=19:39:49.190 +0700 +07:00 232 DST 5 5d|8m|Pia|Eight
1988/09/21 08PM=20:40:50.200 +0800 +08:00 265 --- 6 6d|9m|Sub|Nine
1989/10/22 09PM=21:41:51.210 +0900 +09:00 295 DST 0 0d|10m|Vos|Ten
1990/11/23 10PM=22:42:52.220 +1000 +10:00 327 --- 1 1d|11m|Pon|11en
1991/12/24 11PM=23:43:53.230 +1100 +11:00 358 DST 2 2d|12m|Vto|12ve
1992/01/25 12AM=00:44:54.240 +1200 +12:00 025 --- 3 3d|1m|Sre|One
1993/02/26 01AM=01:45:55.250 +1300 +13:00 057 DST 4 4d|2m|Che|Two
1994/03/27 02AM=02:46:56.260 +1400 +14:00 086 --- 5 5d|3m|Pia|Three
1995/04/28 03AM=03:47:57.270 -1200 -12:00 118 DST 6 6d|4m|Sub|Four
1996/05/29 04AM=04:48:58.280 -1100 -11:00 150 --- 0 0d|5m|Vos|Five
1997/06/30 05AM=05:49:59.290 -1000 -10:00 181 DST 1 1d|6m|Pon|Six
1998/07/31 06AM=06:50:60.300 -0900 -09:00 212 --- 2 2d|7m|Vto|Seven
""".split("\n")[1:-1]; assert output.n==31

date_data["P"]=("---","DST"); date_data["p"] = ("AM","PM")
date_data["D"] = "$Y/$m/$d"; date_data["T"] = "$H:$M:$S"
for i in range(31):
  d = (1968+i,1+i%12,i+1, i%24,20+i,30+i+(i/100.0), (i%27)-12,i%2, i%7, 300+i)
  assert "$D $h$p=$T.$t $Z $z $n $P $w $a|$b|$A|$B".ft(d) == output[i]

t = (9999,12,99, 99,99,99, +359940,9, 6,-1) # month and weekday must be 1..12 0..6
assert "$Y $m $d $H $M $S $w $Z".ft(t) == "9999 12 99 99 99 99 6 +9959" # n XXX

# Functions pad,fit,repl,hms,dhms,wdhms

assert pad("a",3) == "a  "
assert fit("a",3) == "a  "
assert repl("abc","a","x","b","y") == "xyc"
assert hms(100) == (0,1,40)
assert dhms(86401) == (1,0,0,1)
assert wdhms(70*86400) == (10,0,0,0,0)
