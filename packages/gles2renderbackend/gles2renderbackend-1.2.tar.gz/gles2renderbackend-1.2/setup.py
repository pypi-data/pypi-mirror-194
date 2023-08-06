from setuptools import setup, find_packages, Extension
import pybind11

gles2renderbackend_module = Extension(
    'gles2renderbackend',
    sources=['pythongles2renderbackend.cpp'],
    include_dirs=['/usr/include', '.',pybind11.get_include()],
    library_dirs=['/usr/lib64'],
    runtime_library_dirs=['/usr/lib64'],
    libraries=['gles2renderbackend'],
    extra_compile_args=["-std=c++17"]
)

setup(
    name="gles2renderbackend",
    version="1.2",
    description="TestPackage",
    long_description=__doc__,
    packages=find_packages(),
    ext_modules=[gles2renderbackend_module],
    include_package_data=True,
    zip_safe=False,
)
