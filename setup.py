from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'database',
        ['cpp/database.cpp'],
        include_dirs=[pybind11.get_include(), '/usr/include/jsoncpp'],  # Include the jsoncpp headers
        libraries=['jsoncpp'],  # Link against the jsoncpp library
        library_dirs=['/usr/lib'],  # Path to the jsoncpp library (adjust if necessary)
        language='c++'
    ),
]

setup(
    name='InMemoryDB',
    ext_modules=ext_modules,
    zip_safe=False,
)
