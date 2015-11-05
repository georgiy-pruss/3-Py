== What's this ==

https://code.google.com/p/typehack/source/browse/#hg%2Fsrc

"typehack" is a Python 2.7 module to make build-in classes and C-written classes changeable.
By default Python prevents from added, removing or modifying members of C-written classes.
See http://www.python.org/download/releases/2.2/descrintro/#introspection (last paragraph)

> For the curious: there are two reasons why changing built-in classes is disallowed.
> First, it would be too easy to break an invariant of a built-in type that is relied
> upon elsewhere, either by the standard library, or by the run-time code. Second,
> when Python is embedded in another application that creates multiple Python
> interpreters, the built-in class objects (being statically allocated data structures)
> are shared between all interpreters; thus, code running in one interpreter might
> wreak havoc on another interpreter, which is a no-no.

But if you realy need to add some functionality to 3-rd party class and are ok with
Python developers warnings so this module might help you.

Also Guido's words http://code.activestate.com/lists/python-dev/76574/

> This is prohibited intentionally to prevent accidental fatal changes
> to built-in types (fatal to parts of the code that you never though
> of). Also, it is done to prevent the changes to affect different
> interpreters residing in the address space, since built-in types
> (unlike user-defined classes) are shared between all such
> interpreters.

And at http://code.activestate.com/lists/python-dev/89276/

> I should add that this policy is also forced somewhat by the existence
> of the "multiple interpreters in one address space" feature, which is
> used e.g. by mod_python. This feature attempts to provide isolation
> between interpreters to the point that each one can have a completely
> different set of modules loaded and can be working on a totally
> different application. The implementation of CPython shares built-in
> types between multiple interpreters (and it wouldn't be easy to change
> this); if you were able to modify a built-in type from one
> interpreter, all other interpreters would see that same modification.

But if want something realy hard than you can achieve anything.

== Why ==

This POC shows that built-in types could be modified in runtime
without even changing Python source code.

== Usage ==

To have ability modify built-in classes just import "typehack" module.

>>> import typehack

Create custom function to be used as "len" method

>>> def custom_len(obj):
...     return len(obj)
...
>>> list.len = custom_len

Now list is extended with "len" method

>>> [1,2,3].len()
3
>>>

You can't modify already existing type methods. You can't override
list.__len__, dict.__str__, str.find
Also you can't remove members.
