#include <Python.h>

static setattrofunc original_setattr_func = NULL;

void apply_patch();
static int new_setattr_func(PyTypeObject* type, PyObject* name, PyObject* value);

static PyMethodDef THMethods[] =
{
  {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef thmodule =
{
   PyModuleDef_HEAD_INIT,
   "typehack",   /* name of module */
   "allows to add methods to built-in types", /* module documentation, may be NULL */
   -1,   /* size of per-interpreter state of the module,
            or -1 if the module keeps state in global variables. */
   THMethods
};


PyMODINIT_FUNC
PyInit_typehack(void)
{
  PyObject* m;
  m = PyModule_Create(&thmodule);
  if(m == NULL)
    return NULL;
  apply_patch();
  return m;
}

void apply_patch()
{
  original_setattr_func = PyType_Type.tp_setattro;
  PyType_Type.tp_setattro = (setattrofunc)new_setattr_func;
}

static int
new_setattr_func(PyTypeObject* type, PyObject* name, PyObject* value)
{
  int hasItem;
  PyObject* dyn_members_list;
  PyObject* type_dict;

  if(type->tp_flags & Py_TPFLAGS_HEAPTYPE)
    return original_setattr_func((PyObject*)type, name, value);

  type_dict = type->tp_dict;
  hasItem = PyDict_Contains(type_dict, name);
  dyn_members_list = PyDict_GetItemString(type_dict, "__dyn_attrs__");

  if(hasItem == 1)
  {
    /* type already has "name" attribute */
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
      /* Replace attribute */
      if(PyDict_SetItem(type_dict, name, value) < 0)
        return -1;
      /* reset members cache */
      PyType_Modified(type);
      return 0;
    }
    /* "name" is not in "__dyn_attrs__" list. Throw an exception */
    PyErr_Format(PyExc_TypeError,
      "can't set attributes of built-in/extension type '%s'",
      type->tp_name);
    return -1;
  }
  else if(hasItem == 0)
  {
    /* create new attribute */
    if(dyn_members_list == NULL)
    {
      dyn_members_list = PyList_New(0);
      PyDict_SetItemString(type_dict, "__dyn_attrs__", dyn_members_list);
      Py_INCREF(dyn_members_list);
    }
    PyList_Append(dyn_members_list, name); /* add "name" to list of dynamic attributes */
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

int PyList_Contains(PyObject* lst, PyObject* value)
{
  Py_ssize_t index;
  Py_ssize_t len = PyList_Size(lst);
  PyObject* cmp_result = NULL;
  for(index=0; index<len; ++index)
  {
    cmp_result = PyObject_RichCompare(value, PyList_GetItem(lst, index), Py_EQ);
    if( cmp_result == NULL )
      return -1;
    if( cmp_result == Py_True )
    {
      Py_DECREF(cmp_result);
      return 1; /* Found */
    }
    Py_DECREF(cmp_result);
  }
  return 0; /* Not found */
}
