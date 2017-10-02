Cython could use C and C library to accelerate the speed.
use it by follow command compile:

```
python3 setup.py build_ext --inplace
```

then you can import the producted *.os file ,and use the function included.

but if you want to accelerate,you must adjust the data type by use **cdef** args.