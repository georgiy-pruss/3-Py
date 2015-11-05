/* http://habrahabr.ru/post/142034/
 * by http://habrahabr.ru/users/sheknitrtch/
 * 2012.04.13
 */

#include <Python.h>

static setattrofunc original_setattr_func = NULL;

void apply_patch();
static int new_setattr_func(PyTypeObject *type, PyObject *name, PyObject *value);

PyMODINIT_FUNC
inittypehack(void)
{
  PyObject *m;
  m = Py_InitModule("typehack", NULL);
  if(m == NULL)
    return;
  apply_patch();
}

void apply_patch()
{
  original_setattr_func = PyType_Type.tp_setattro;
  PyType_Type.tp_setattro = new_setattr_func;
}

static int
new_setattr_func(PyTypeObject *type, PyObject *name, PyObject *value)
{
  if(!(type->tp_flags & Py_TPFLAGS_HEAPTYPE))
  {
    PyObject *type_dict = type->tp_dict;
    int hasItem;
    PyObject *dyn_members_list;

    hasItem = PyDict_Contains(type_dict, name);
    dyn_members_list = PyDict_GetItemString(type_dict, "__dyn_attrs__");

    if(hasItem == 1)
    {
      //type already has "name" attribute
      if(dyn_members_list==NULL)
      {
        /* "__dyn_attrs__" is not created yet. Do not replace type member */
        PyErr_Format(PyExc_TypeError,
          "can't set attributes of built-in/extension type '%s'",
          type->tp_name);
        return -1;
      }

      if(PyList_Contains(dyn_members_list, name)==1)
      {
        //Replace attribute
        if(PyDict_SetItem(type_dict, name, value) < 0)
          return -1;
        else
        {
          /* reset members cache */
          PyType_Modified(type);
          return 0;
        }
      }
      else
      {
        //"name" is not in "__dyn_attrs__" list. Throw an exception
        PyErr_Format(PyExc_TypeError,
          "can't set attributes of built-in/extension type '%s'",
          type->tp_name);
        return -1;
      }
    }
    else if(hasItem == 0)
    {
      //creating new attribute
      if(dyn_members_list == NULL)
      {
        dyn_members_list = PyList_New(0);
        PyDict_SetItemString(type_dict, "__dyn_attrs__", dyn_members_list);
        Py_INCREF(dyn_members_list);
      }

      PyList_Append(dyn_members_list, name); //add "name" to list of dynamic attributes
      if( PyDict_SetItem(type_dict, name, value) < 0)
        return -1;
      /* reset members cache */
      PyType_Modified(type);
      return 0;
    }
    else
    {
      return hasItem;
    }
  }
  else
  {
    return original_setattr_func(type, name, value);
  }
}

int PyDict_ContainsString(PyObject* d, const char* key)
{
  PyObject* kv = PyString_FromString(key);
  int result;
  if(kv == NULL)
    return -1;
  result = PyDict_Contains(d, kv);
  Py_DECREF(kv);
  return result;
}

int PyList_Contains(PyObject *lst, PyObject *value)
{
  Py_ssize_t index;
  Py_ssize_t len = PyList_Size(lst);
  int cmp_result;
  for(index=0; index<len; ++index)
  {
    if( PyObject_Cmp(value, PyList_GetItem(lst, index), &cmp_result) == -1)
      return -1;
    if( cmp_result == 0)
      return 1; //Found
  }
  return 0; //Not found
}
