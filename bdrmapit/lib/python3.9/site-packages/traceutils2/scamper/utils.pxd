from traceutils2.scamper.hop cimport Reader, TraceFType

cpdef Reader reader(str filename, TraceFType ftype=*, bint safe=*, bint parallel_read=*);