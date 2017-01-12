<pre>
<n    range(n)      maybe ..n
<=n   range(n+1)          ...n

#hhh  hex.number          b#xxx   base b number
#'hh' hex.string, bytes
#<...> #(...) #[...] #{...} comment
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

x?y!z      if x: y, else: z

if'str'
fn'str'

1 2 3      [1,2,3]

for v e:   for v in e:

if expr as var: ...
while expr as var: ...

str(args)  str%(args)
str n      str%n

/\ x, y: expr    lambda

=expr      return expr

cities =:
    "Киев"
    "Chișineu"
    "București"
    # dicts?

#def macro(x,y): ....
#def macro [...]
#ifdef macro
#else
#endif

</pre>
