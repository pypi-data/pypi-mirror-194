from glob import glob
import os
from setuptools import setup, find_packages
import build_utils as _bu
import colemen_utilities.build_utils.general as _gen
VERSION='2.18.85'
DESCRIPTION = 'Colemen Utils'
LONG_DESCRIPTION = 'Colemen Utils is a composite library of shit I find useful.'

PY_MODULES = _gen.list_py_modules(
    f"{os.getcwd()}/colemen_utilities",
    additions=['colemen_utils','colemen_config']
    )
_bu.purge_dist()

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="colemen_utils",
    version=VERSION,
    author="Colemen Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    py_modules=PY_MODULES,
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=[
        'secure_delete',
        'ftputil',
        'ffmpeg-python',
        'pillow',
        'faker',
        'iptcinfo3',
        'patool',
        'pyparsing',
        'sqlparse',
        'colorama',
        'lxml',
        'mysql-connector-python',
        'exrex',
        'pyyaml',
        'inflect',
        'cerberus',
    ],
    data_files=[
        ('Lib/site-packages/colemen_utilities/documentation', glob('documentation/*.md')),
        ('Lib/site-packages/colemen_utilities/build_utils', glob('colemen_utilities/build_utils/*.template')),
        # (
        #     'Lib/site-packages/colemen_utilities/documentation',
        # ['colemen_utilities/build_utils/build_utils.html']
        # 'colemen_utilities/build_utils/*.template'
        # )
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

