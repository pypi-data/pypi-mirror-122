# -*- coding: utf-8 -*-

import setuptools

from lynxinven.base import LYNXINVEN_PYTHON_VERSION

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="lynxinven",

    version=LYNXINVEN_PYTHON_VERSION,

    author="Jason Menzies",

    author_email="info@lynxsolve.com",

    description="Python interface for LynxInven inventory management system",

    long_description=long_description,

    long_description_content_type='text/markdown',

    keywords="bom, bill of materials, stock, inventory, management, barcode",

    url="https://github.com/Lynx-Solve/lynxinven-python/",

    license="MIT",

    packages=setuptools.find_packages(),

    install_requires=[
        "requests"
    ],

    setup_requires=[
        "wheel",
    ],

    python_requires=">=3.6"
)
