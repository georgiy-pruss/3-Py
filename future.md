<pre>
&lt;n    range(n)      maybe ..n
&lt;=n   range(n+1)          ...n

#hhh  hex.number          b#xxx   base b number
#'hh' hex.string, bytes
#&lt;...> #(...) #[...] #{...} comment
#!... # ...     usual Python comment

binops              unops

++ append
-- remove all
^^ starts with     ^^ upper
$$ ends with
~~ find match

~= approx eq

%% replace

                    $a   len(a)
\  join a\s         \a   a\''
\\ split
                    ?n   random int 0..n-1
                    ?1   random float 0..1
                    !x   not x (but: !x in y ≡ not x in y)

x?y!z      if x: y, else: z

if'str'
fn'str'

1 2 3      [1,2,3]

for v e:   for v in e:

if expr as var: ...
while expr as var: ...

str(args)  str%(args)
str n      str%n

(x, y): expr    lambda x,y: expr

=expr      return expr

cities =:
    "Киев"
    "Chișineu"
    "București"
    # dicts?

reduce:
#(fn(x,y) for y in iter [if ...], from x0])
#(x+y*y for y in array, 0)

#def macro(x,y): ....
#def macro [...]
#ifdef macro
#else
#endif

</pre>
