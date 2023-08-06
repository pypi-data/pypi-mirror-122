Introduction
============
This package provides a Python API to open, create, and manipulate [NeXus 
data](http://www.nexusformat.org/) written in the HDF5 format. The 
'nexusformat' package provides the underlying API for 
[NeXpy](http://nexpy.github.io/nexpy), which provides a GUI interface for
visualizing and analyzing NeXus data. 

The latest development version is always available from [NeXpy's GitHub
repository](https://github.com/nexpy/nexusformat).

Installing and Running
======================
Released versions of `nexusformat` can be installed using either

```
    $ pip install nexusformat
```

or

```
    $ easy_install nexusformat
```

If you have an Anaconda installation, use::

```
    $ conda install -c nexpy nexusformat
```

The source code can be downloaded from the NeXpy Git repository:

```
    $ git clone http://github.com/nexpy/nexusformat.git
```

To install in the standard Python location:

```
    $ python setup.py install
```

To install in an alternate location:

```
    $ python setup.py install --prefix=/path/to/installation/dir
```

Prerequisites
=============
The following libraries are used by the full installation of NeXpy. There is 
more details of the nature of these dependencies in the 
[NeXpy documentation](http://nexpy.github.io/nexpy).

* h5py                 http://www.h5py.org
* numpy                http://numpy.org

User Support
============
Consult the [NeXpy documentation](http://nexpy.github.io/nexpy) for details 
of both the Python command-line API and how to use the NeXpy GUI. If you have 
any general questions concerning the use of NeXpy, please address 
them to the 
[NeXus Mailing List](http://download.nexusformat.org/doc/html/mailinglist.html). 
If you discover any bugs, please submit a 
[Github issue](https://github.com/nexpy/nexusformat/issues), preferably with 
relevant tracebacks.
