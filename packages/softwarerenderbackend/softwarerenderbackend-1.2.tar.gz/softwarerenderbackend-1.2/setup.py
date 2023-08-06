from setuptools import setup, find_packages, Extension
import pybind11

softwarerenderbackend_module = Extension(
    'softwarerenderbackend',
    sources=['pythonsoftwarerenderbackend.cpp'],
    include_dirs=['/usr/include', '.',pybind11.get_include()],
    library_dirs=['/usr/lib64'],
    runtime_library_dirs=['/usr/lib64'],
    libraries=['softwarerenderbackend'],
    extra_compile_args=["-std=c++17"]
)

setup(
    name="softwarerenderbackend",
    version="1.2",
    description="TestPackage",
    long_description=__doc__,
    packages=find_packages(),
    ext_modules=[softwarerenderbackend_module],
    include_package_data=True,
    zip_safe=False,
)
