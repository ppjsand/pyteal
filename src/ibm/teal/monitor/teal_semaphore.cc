// begin_generated_IBM_copyright_prolog
//
// This is an automatically generated copyright prolog.
// After initializing,  DO NOT MODIFY OR MOVE
// ================================================================
//
// (C) Copyright IBM Corp.  2010,2011
// Eclipse Public License (EPL)
//
// ================================================================
//
// end_generated_IBM_copyright_prolog

/*--------------------------------------------------------------------*/
/*  Includes                                                          */
/*--------------------------------------------------------------------*/

#include <Python.h>
#include <structmember.h>

#include "Semaphore.h"

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

typedef struct {
    PyObject_HEAD
    TEAL::Semaphore* s;
} SemaphoreObject;

/*--------------------------------------------------------------------*/
/*  Constants                                                         */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Macros                                                            */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Internal Function Prototypes                                      */
/*--------------------------------------------------------------------*/

static PyObject* Semaphore_new(PyTypeObject *type, PyObject *args, PyObject *kwargs);
static void Semaphore_dealloc(SemaphoreObject* self);

static PyObject* Semaphore_post(SemaphoreObject* self);
static PyObject* Semaphore_wait(SemaphoreObject* self);

/*--------------------------------------------------------------------*/
/*  Global Variables                                                  */
/*--------------------------------------------------------------------*/

static PyMethodDef teal_semaphore_methods[] = {
    {NULL}
};

static PyMethodDef Semaphore_methods[] = {
    {"post", (PyCFunction)Semaphore_post, METH_NOARGS, "Post data has been inserted into DB"},
    {"wait", (PyCFunction)Semaphore_wait, METH_NOARGS, "Wait for data to be inserted into DB"},
    {NULL}
};

static PyTypeObject teal_semaphore_SemaphoreType = {
    PyObject_HEAD_INIT(NULL)
    0,                                         /*ob_size*/
    "teal_semaphore.Semaphore",                /*tp_name*/
    sizeof(SemaphoreObject),                   /*tp_basicsize*/
    0,                                         /*tp_itemsize*/
    (destructor)Semaphore_dealloc,             /*tp_dealloc*/
    0,                                         /*tp_print*/
    0,                                         /*tp_getattr*/
    0,                                         /*tp_setattr*/
    0,                                         /*tp_compare*/
    0,                                         /*tp_repr*/
    0,                                         /*tp_as_number*/
    0,                                         /*tp_as_sequence*/
    0,                                         /*tp_as_mapping*/
    0,                                         /*tp_hash */
    0,                                         /*tp_call*/
    0,                                         /*tp_str*/
    0,                                         /*tp_getattro*/
    0,                                         /*tp_setattro*/
    0,                                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,                        /*tp_flags*/
    "TEAL Database Notification Semaphore",    /* tp_doc */
    0,                                         /* tp_traverse */
    0,                                         /* tp_clear */
    0,                                         /* tp_richcompare */
    0,                                         /* tp_weaklistoffset */
    0,                                         /* tp_iter */
    0,                                         /* tp_iternext */
    Semaphore_methods,                         /* tp_methods */
    0,                                         /* tp_members */
    0,                                         /* tp_getset */
    0,                                         /* tp_base */
    0,                                         /* tp_dict */
    0,                                         /* tp_descr_get */
    0,                                         /* tp_descr_set */
    0,                                         /* tp_dictoffset */
    0,                                         /* tp_init */
    0,                                         /* tp_alloc */
    Semaphore_new,                             /* tp_new */
};

/*--------------------------------------------------------------------*/
/* >>> Function <<<                                                   */
/*--------------------------------------------------------------------*/

static void Semaphore_dealloc(SemaphoreObject* self)
{
    //printf("delete: self->s = %p\n",self->s);
    delete self->s;
    self->ob_type->tp_free((PyObject*)self);
}

/*--------------------------------------------------------------------*/

static PyObject* Semaphore_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    SemaphoreObject* self;

    int role = TEAL::Semaphore::SERVER;
    char* name = NULL;
    int project = -1;

    if (!PyArg_ParseTuple(args,"|isi",&role,&name,&project)) {
        return NULL;
    }

    self = (SemaphoreObject*)type->tp_alloc(type, 0);
    if (self != NULL) {
    	if (name == NULL) { // if name not specified, project is ignored
    		self->s = new TEAL::Semaphore(static_cast<TEAL::Semaphore::Role>(role));
    	} else if ((name != NULL) && (project == -1)) {
    		self->s = new TEAL::Semaphore(static_cast<TEAL::Semaphore::Role>(role),name);
    	} else  {// (name != NULL && (project != 1)
    		self->s = new TEAL::Semaphore(static_cast<TEAL::Semaphore::Role>(role),name,project);
    	}
        //printf("new: self->s = %p\n",self->s);
    }

    return (PyObject*)self;
}

/*--------------------------------------------------------------------*/

static PyObject* Semaphore_wait(SemaphoreObject* self) {
    int rc = 0;
    Py_BEGIN_ALLOW_THREADS
    rc = self->s->wait();
    Py_END_ALLOW_THREADS
    return Py_BuildValue("i",rc);
}

/*--------------------------------------------------------------------*/

static PyObject* Semaphore_post(SemaphoreObject* self) {
    Py_BEGIN_ALLOW_THREADS
    self->s->post();
    Py_END_ALLOW_THREADS
    Py_INCREF(Py_None);
    return Py_None;
}

/*--------------------------------------------------------------------*/

PyMODINIT_FUNC
initteal_semaphore(void) {
	if (PyType_Ready(&teal_semaphore_SemaphoreType) < 0)
        return;

    PyObject* m = Py_InitModule3("teal_semaphore", teal_semaphore_methods, "Teal DB notification Semaphore module");

    Py_INCREF(&teal_semaphore_SemaphoreType);
    PyModule_AddObject(m, "Semaphore", (PyObject*)&teal_semaphore_SemaphoreType);
    PyModule_AddIntConstant(m, "CLIENT", TEAL::Semaphore::CLIENT);
    PyModule_AddIntConstant(m, "SERVER", TEAL::Semaphore::SERVER);
}




