'''
Created on 15 sep. 2015

@author: Brian
'''

from distutils.core import setup
import py2exe
import matplotlib

opts={
         'py2exe': {'bundle_files': 2,
                    'compressed': True,
                    
                    'packages' :  ['matplotlib', 'pytz', 'core', 'utils'],
                    "includes" : ["matplotlib.backends.backend_tkagg",],
                    
                    'excludes': ['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg', "matplotlib.numerix.fft","sip", "PyQt4._qt",
                                 "matplotlib.backends.backend_qt4agg",
                                 "matplotlib.numerix.linear_algebra", "matplotlib.numerix.random_array",

                                 '_fltkagg', '_gtk','_gtkcairo', "Tkconstants","Tkinter","tcl"],
                    'dll_excludes': ['libgdk-win32-2.0-0.dll',
                                   'libgobject-2.0-0.dll',
                                   'libgdk_pixbuf-2.0-0.dll',
                                   'libgtk-win32-2.0-0.dll',
                                   'libglib-2.0-0.dll',
                                   'libcairo-2.dll',
                                   'libpango-1.0-0.dll',
                                   'libpangowin32-1.0-0.dll',
                                   'libpangocairo-1.0-0.dll',
                                   'libglade-2.0-0.dll',
                                   'libgmodule-2.0-0.dll',
                                   'libgthread-2.0-0.dll',
                                   'QtGui4.dll', 'QtCore.dll',
                                   'QtCore4.dll',
                                   'tcl86t.dll',
                                   'tk86t.dll'
                                  ],
                    }
}
data_files=matplotlib.get_py2exe_datafiles()

zipfile=None

setup(console=["main.py"], options=opts, data_files=data_files, zipfile=None)
