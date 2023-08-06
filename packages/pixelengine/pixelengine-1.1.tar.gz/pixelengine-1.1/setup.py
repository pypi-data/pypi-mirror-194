from setuptools import setup, find_packages, Extension
import pybind11

pixelengine_module = Extension(
    'pixelengine',
    sources=['pythonpixelengine.cpp'],
    include_dirs=['/usr/include', '.',pybind11.get_include()],
    library_dirs=['/usr/lib64'],
    runtime_library_dirs=['/usr/lib64'],
    libraries=['pixelengine'],
    extra_compile_args=["-std=c++17"],
)

setup(
    name="pixelengine",
    version="1.1",
    description="RT",
    long_description=__doc__,
    packages=find_packages(),
    install_requires=['eglrendercontext'],
    ext_modules=[pixelengine_module],
    include_package_data=True,
    zip_safe=False,
)
