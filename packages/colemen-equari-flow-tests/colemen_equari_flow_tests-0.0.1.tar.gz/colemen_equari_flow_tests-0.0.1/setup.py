from setuptools import setup, find_packages
import colemen_utils as _c
# import build_utils as _bu
import os

VERSION = '0.0.1'
DESCRIPTION = 'EquariFlowTests'
LONG_DESCRIPTION = 'EquariFlowTests'

PY_MODULES = _c.build.list_py_modules(
    f"{os.getcwd()}/apricity",
    additions=["main"]
    )
_c.build.purge_dist()


# Setting up
setup(
    name="colemen_equari_flow_tests",
    version=VERSION,
    author="Colemen Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=PY_MODULES,
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=[
        'colemen_utils',
    ],

    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
