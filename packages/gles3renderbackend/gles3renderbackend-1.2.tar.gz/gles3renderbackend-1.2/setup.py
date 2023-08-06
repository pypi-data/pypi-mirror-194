from setuptools import setup, find_packages, Extension
import pybind11

gles3renderbackend_module = Extension(
    'gles3renderbackend',
    sources=['pythongles3renderbackend.cpp'],
    include_dirs=['/usr/include', '.',pybind11.get_include()],
    library_dirs=['/usr/lib64'],
    runtime_library_dirs=['/usr/lib64'],
    libraries=['gles3renderbackend'],
    extra_compile_args=["-std=c++17"]
)

setup(
    name="gles3renderbackend",
    version="1.2",
    description="TestPackage",
    long_description=__doc__,
    packages=find_packages(),
    ext_modules=[gles3renderbackend_module],
    include_package_data=True,
    zip_safe=False,
)
