from setuptools import setup, find_packages

setup(
    name='afoone_calculadora',
    packages=['calculadora'],
    include_package_data=True,  # para que se incluyan archivos sin extension .py, si solo hay .py no es necesario
    version='0.1',
    description='Calculator package for testing pypi',
    author='Alfonso Tienda',
    author_email="afoone@hotmail.com",
    license="GPLv3",
    url="https://github.com/afoone/calculadora",
    classifiers=["Programming Language :: Python :: 3", \
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)", \
                 "Development Status :: 3 - Alpha",
                 "Intended Audience :: Education", \
                 "Operating System :: OS Independent"],
)
