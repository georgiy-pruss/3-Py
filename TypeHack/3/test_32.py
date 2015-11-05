import unittest
import sys
sys.path.append("../release");

class TestSequenceFunctions(unittest.TestCase):
  def setUp(self):
    import typehack

  def test_list(self):
    with self.assertRaises(AttributeError):
      [1,2,3].len()

    def custom_len(obj):
      return len(obj)

    list.len = custom_len
    self.assertTrue('len' in list.__dict__)
    self.assertEqual(['a', 'b', 'c'].len(), 3)


  def test_map(self):
    def common_map(_list, function):
      return list(map(function, _list))
    list.map = common_map
    data = ['Tinker', 'Tailor', 'Solder', 'Spy']
    data = data.map(str.__len__)
    self.assertEqual(data, [6,6,6,3])

  def test_property(self):
    size = property(len)
    dict.size = size
    data = {'a':1, 'b':2, 'c':3}
    self.assertEqual(data.size, 3)
    data['d'] = -1
    self.assertEqual(data.size, 4)

  def test_forbidModification(self):
    with self.assertRaises(TypeError):
      dict.__len__ = None;

  def test_allowRewriteMember(self):
    with self.assertRaises(AttributeError):
      set.foo()
    def foo1(self):
      return "foo1"

    set.foo = foo1
    x = set(['red', 'green', 'blue'])
    self.assertEqual(x.foo(), "foo1")

    self.assertTrue("foo" in set.__dyn_attrs__)

    #replace custom method "foo" with new value
    def foo2(self):
      return "foo2"

    set.foo = foo2
    self.assertEqual(x.foo(), "foo2")

if __name__ == '__main__':
  unittest.main()
