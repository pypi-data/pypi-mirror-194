/*
# This file is part of the Astrometry.net suite.
# Licensed under a 3-clause BSD style license - see LICENSE
 */
%module(package="lanczos") lanczos

%include <typemaps.i>
%include <cstring.i>
%include <exception.i>

%{
// numpy.
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

#include <stdint.h>
#include <stdlib.h>
#include <math.h>

#define true 1
#define false 0

// For sip.h
static void checkorder(int i, int j) {
    assert(i >= 0);
    assert(i < SIP_MAXORDER);
    assert(j >= 0);
    assert(j < SIP_MAXORDER);
}

// From index.i:
/**
For returning single codes and quads as python lists, do something like this:

%typemap(out) float [ANY] {
  int i;
  $result = PyList_New($1_dim0);
  for (i = 0; i < $1_dim0; i++) {
    PyObject *o = PyFloat_FromDouble((double) $1[i]);
    PyList_SetItem($result,i,o);
  }
}
**/

double* code_alloc(int DC) {
	 return malloc(DC * sizeof(double));
}
void code_free(double* code) {
	 free(code);
}
double code_get(double* code, int i) {
	return code[i];
}

/*
long qidxfile_addr(qidxfile* qf) {
	 return (long)qf;
}
 */

%}

%init %{
      // numpy
      import_array();
%}

// Things in keywords.h (used by healpix.h)
#define Const
#define WarnUnusedResult
#define InlineDeclare
#define Flatten
#define ASTROMETRY_KEYWORDS_H
#define ATTRIB_FORMAT(x,y,z)

%inline %{
#define ERR(x, ...)                             \
    printf(x, ## __VA_ARGS__)

    static void print_array(PyObject* arr) {
        PyArrayObject *obj;
        int i, N;
        PyArray_Descr *desc;
        printf("Array: %p\n", arr);
        if (!arr) return;
        if (!PyArray_Check(arr)) {
            printf("  Not a Numpy Array\n");
            if (arr == Py_None)
                printf("  is None\n");
            return;
        }
        obj = (PyArrayObject*)arr;

        printf("  Contiguous: %s\n",
               PyArray_ISCONTIGUOUS(obj) ? "yes" : "no");
        printf("  Writeable: %s\n",
               PyArray_ISWRITEABLE(obj) ? "yes" : "no");
        printf("  Aligned: %s\n",
               PyArray_ISALIGNED(obj) ? "yes" : "no");
        printf("  C array: %s\n",
               PyArray_ISCARRAY(obj) ? "yes" : "no");

        //printf("  typeobj: %p (float is %p)\n", arr->typeobj,
        //&PyFloat_Type);

        printf("  data: %p\n", PyArray_DATA(obj));
        printf("  N dims: %i\n", PyArray_NDIM(obj));
        N = PyArray_NDIM(obj);
        for (i=0; i<N; i++)
            printf("  dim %i: %i\n", i, (int)PyArray_DIM(obj, i));
        for (i=0; i<N; i++)
            printf("  stride %i: %i\n", i, (int)PyArray_STRIDE(obj, i));
        desc = PyArray_DESCR(obj);
        printf("  descr kind: '%c'\n", desc->kind);
        printf("  descr type: '%c'\n", desc->type);
        printf("  descr byteorder: '%c'\n", desc->byteorder);
        printf("  descr elsize: %i\n", desc->elsize);
    }


    #define LANCZOS_INTERP_FUNC lanczos5_interpolate
    #define L 5
        static int LANCZOS_INTERP_FUNC(PyObject* np_ixi, PyObject* np_iyi,
                                       PyObject* np_dx, PyObject* np_dy,
                                       PyObject* loutputs, PyObject* linputs);
    #include "lanczos.i"
    #undef LANCZOS_INTERP_FUNC
    #undef L

    #define LANCZOS_INTERP_FUNC lanczos3_interpolate
    #define L 3
        static int LANCZOS_INTERP_FUNC(PyObject* np_ixi, PyObject* np_iyi,
                                       PyObject* np_dx, PyObject* np_dy,
                                       PyObject* loutputs, PyObject* linputs);
    #include "lanczos.i"
    #undef LANCZOS_INTERP_FUNC
    #undef L

    static int lanczos5_filter(PyObject* py_dx, PyObject* py_f) {
        npy_intp N;
        npy_intp i;
        float* dx;
        float* f;

        PyArrayObject *np_dx = (PyArrayObject*)py_dx;
        PyArrayObject *np_f  = (PyArrayObject*)py_f;

        if (!PyArray_Check(np_dx) ||
            !PyArray_Check(np_f ) ||
            !PyArray_ISNOTSWAPPED(np_dx) ||
            !PyArray_ISNOTSWAPPED(np_f ) ||
            !PyArray_ISFLOAT(np_dx) ||
            !PyArray_ISFLOAT(np_f ) ||
            (PyArray_ITEMSIZE(np_dx) != sizeof(float)) ||
            (PyArray_ITEMSIZE(np_f ) != sizeof(float)) ||
            !(PyArray_NDIM(np_dx) == 1) ||
            !(PyArray_NDIM(np_f ) == 1) ||
            !PyArray_ISCONTIGUOUS(np_dx) ||
            !PyArray_ISCONTIGUOUS(np_f ) ||
            !PyArray_ISWRITEABLE(np_f)
            ) {
            ERR("Arrays aren't right type\n");
            return -1;
        }
        N = PyArray_DIM(np_dx, 0);
        if (PyArray_DIM(np_f, 0) != N) {
            ERR("Input and output must have same dimensions\n");
            return -1;
        }
        dx = PyArray_DATA(np_dx);
        f = PyArray_DATA(np_f);
        const double fifthpi = M_PI / 5.0;
        const double pisq = M_PI * M_PI;
        const double fiveopisq = 5. / pisq;
        for (i=N; i>0; i--, dx++, f++) {
            double x = *dx;
            if (x < -5.0 || x > 5.0) {
                *f = 0.0;
            } else if (x == 0) {
                *f = 1.0;
            } else {
                *f = fiveopisq * sin(M_PI * x) * sin(fifthpi * x) / (x * x);
            }
        }
        return 0;
    }

    static int lanczos3_filter(PyObject* py_dx, PyObject* py_f) {
        npy_intp N;
        npy_intp i;
        float* dx;
        float* f;

        PyArrayObject *np_dx = (PyArrayObject*)py_dx;
        PyArrayObject *np_f  = (PyArrayObject*)py_f;

        if (!PyArray_Check(np_dx) ||
            !PyArray_Check(np_f ) ||
            !PyArray_ISNOTSWAPPED(np_dx) ||
            !PyArray_ISNOTSWAPPED(np_f ) ||
            !PyArray_ISFLOAT(np_dx) ||
            !PyArray_ISFLOAT(np_f ) ||
            (PyArray_ITEMSIZE(np_dx) != sizeof(float)) ||
            (PyArray_ITEMSIZE(np_f ) != sizeof(float)) ||
            !(PyArray_NDIM(np_dx) == 1) ||
            !(PyArray_NDIM(np_f ) == 1) ||
            !PyArray_ISCONTIGUOUS(np_dx) ||
            !PyArray_ISCONTIGUOUS(np_f ) ||
            !PyArray_ISWRITEABLE(np_f)
            ) {
            ERR("Arrays aren't right type\n");
            return -1;
        }
        N = PyArray_DIM(np_dx, 0);
        if (PyArray_DIM(np_f, 0) != N) {
            ERR("Input and output must have same dimensions\n");
            return -1;
        }
        dx = PyArray_DATA(np_dx);
        f = PyArray_DATA(np_f);
        const double thirdpi = M_PI / 3.0;
        const double pisq = M_PI * M_PI;
        const double threeopisq = 3. / pisq;
        for (i=N; i>0; i--, dx++, f++) {
            double x = *dx;
            if (x < -3.0 || x > 3.0) {
                *f = 0.0;
            } else if (x == 0) {
                *f = 1.0;
            } else {
                *f = threeopisq * sin(M_PI * x) * sin(thirdpi * x) / (x * x);
            }
        }
        return 0;
    }

    static int lanczos3_filter_table(PyObject* py_dx, PyObject* py_f, int rangecheck) {
        npy_intp N;
        npy_intp i;
        float* dx;
        float* f;

        PyArrayObject *np_dx = (PyArrayObject*)py_dx;
        PyArrayObject *np_f  = (PyArrayObject*)py_f;

        // Nlutunit is number of bins per unit x
        static const int Nlutunit = 1024;
        static const float lut0 = -4.;
        static const int Nlut = 8192; //8 * Nlutunit;
        // We want bins to go from -4 to 4 (Lanczos-3 range of -3 to 3, plus some buffer)
        // [Nlut]
        static float lut[8192];
        static int initialized = 0;

        if (!initialized) {
            for (i=0; i<(Nlut); i++) {
                float x,f;
                x = (lut0 + (i / (float)Nlutunit));
                if (x <= -3.0 || x >= 3.0) {
                    f = 0.0;
                } else if (x == 0) {
                    f = 1.0;
                } else {
                    f = 3. * sin(M_PI * x) * sin(M_PI / 3.0 * x) / (M_PI * M_PI * x * x);
                }
                lut[i] = f;
            }
            initialized = 1;
        }

        if (!PyArray_Check(np_dx) ||
            !PyArray_Check(np_f )) {
            ERR("Array check\n");
        }
        if (!PyArray_ISNOTSWAPPED(np_dx) ||
            !PyArray_ISNOTSWAPPED(np_f )) {
            ERR("Swapped\n");
        }
        if (!PyArray_ISFLOAT(np_dx) ||
            !PyArray_ISFLOAT(np_f )) {
            ERR("Float\n");
        }
        if ((PyArray_ITEMSIZE(np_dx) != sizeof(float)) ||
            (PyArray_ITEMSIZE(np_f ) != sizeof(float))) {
            ERR("sizeof float\n");
        }
        if ((PyArray_ITEMSIZE(np_dx) != sizeof(float))) {
            ERR("sizeof dx %i\n", (int)PyArray_ITEMSIZE(np_dx));
        }
        if ((PyArray_ITEMSIZE(np_f ) != sizeof(float))) {
            ERR("sizeof f %i\n", (int)PyArray_ITEMSIZE(np_f));
        }
        if (!(PyArray_NDIM(np_dx) == 1) ||
            !(PyArray_NDIM(np_f ) == 1)) {
            ERR("one-d\n");
        }
        if (!PyArray_ISCONTIGUOUS(np_dx) ||
            !PyArray_ISCONTIGUOUS(np_f )) {
            ERR("contig\n");
        }
        if (!PyArray_ISWRITEABLE(np_f)) {
            ERR("writable\n");
        }


        if (!PyArray_Check(np_dx) ||
            !PyArray_Check(np_f ) ||
            !PyArray_ISNOTSWAPPED(np_dx) ||
            !PyArray_ISNOTSWAPPED(np_f ) ||
            !PyArray_ISFLOAT(np_dx) ||
            !PyArray_ISFLOAT(np_f ) ||
            (PyArray_ITEMSIZE(np_dx) != sizeof(float)) ||
            (PyArray_ITEMSIZE(np_f ) != sizeof(float)) ||
            !(PyArray_NDIM(np_dx) == 1) ||
            !(PyArray_NDIM(np_f ) == 1) ||
            !PyArray_ISCONTIGUOUS(np_dx) ||
            !PyArray_ISCONTIGUOUS(np_f ) ||
            !PyArray_ISWRITEABLE(np_f)
            ) {
            ERR("Arrays aren't right type\n");
            return -1;
        }
        N = PyArray_DIM(np_dx, 0);
        if (PyArray_DIM(np_f, 0) != N) {
            ERR("Input and output must have same dimensions\n");
            return -1;
        }
        dx = PyArray_DATA(np_dx);
        f = PyArray_DATA(np_f);
        if (rangecheck) {
            for (i=N; i>0; i--, dx++, f++) {
                float x = *dx;
                int li = (int)((x - lut0) * Nlutunit);
                if ((li < 0) || (li >= Nlut)) {
                    *f = 0.0;
                } else {
                    *f = lut[li];
                }
            }
        } else {
            for (i=N; i>0; i--, dx++, f++) {
                float x = *dx;
                int li = (int)((x - lut0) * Nlutunit);
                *f = lut[li];
            }
        }
        return 0;
    }


%}

