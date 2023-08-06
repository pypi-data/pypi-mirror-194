from setuptools import setup, find_packages, Extension
import pybind11

eglrendercontext_module = Extension(
    'eglrendercontext',
    sources=['pythoneglrendercontext.cpp'],
    include_dirs=['/usr/include', '.',pybind11.get_include()],
    library_dirs=['/usr/lib64'],
    runtime_library_dirs=['/usr/lib64'],
    libraries=['eglrendercontext'],
    extra_compile_args=["-std=c++17"]
)

setup(
    name="eglrendercontext",
    version="1.2",
    description="TestPackage",
    long_description=__doc__,
    packages=find_packages(),
    ext_modules=[eglrendercontext_module],
    include_package_data=True,
    zip_safe=False,
)
