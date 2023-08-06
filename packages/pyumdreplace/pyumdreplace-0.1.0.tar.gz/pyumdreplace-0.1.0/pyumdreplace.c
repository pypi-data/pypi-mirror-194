#include <Python.h>

void Title(void);
void Usage(void);
void Replace(char *isoname, char *oldname, char *newname);

static PyObject *method_run(PyObject *self, PyObject *args, PyObject *kwargs)
{
    char *imagename = NULL;
    char *filename = NULL;
    char *newfile = NULL;

    static char *kwlist[] = {"imagename", "filename", "newfile",
                                NULL};

    if(!PyArg_ParseTupleAndKeywords(args, kwargs, "sss", kwlist,
                                    &imagename, &filename, &newfile))
    {
        Title();
        Usage();
        return NULL;
    }

    Replace(imagename, filename, newfile);
    return PyBool_FromLong(1);
}

static PyMethodDef PyumdreplaceMethods[] = {
    {"run", (PyCFunction)method_run, METH_VARARGS | METH_KEYWORDS, "Python interface for UMD-replace."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef pyumdreplacemodule = {
    PyModuleDef_HEAD_INIT,
    "pyumdreplace",
    "Python interface for UMD-replace.",
    -1,
    PyumdreplaceMethods
};

PyMODINIT_FUNC PyInit_pyumdreplace(void)
{
    return PyModule_Create(&pyumdreplacemodule);
}
