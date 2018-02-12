#!/usr/bin/env python

from distutils.core import setup


def get_description():
    import os
    pth = os.path.join(
        os.path.dirname(os.path.normpath(__file__)),
        'README.md')

    lines = []
    with open(pth, 'r') as f:
        lines = f.readlines()[1:]

    return "".join(
        lines
    )


setup(
    name="django-composition",
    version="0.2.1",

    license="New BSD License",

    author='Alex Koshelev',
    author_email="daevaorn@gmail.com",

    url="http://bitbucket.org/daevaorn/django-composition/",

    packages=[
        "composition",
        "composition.shortcuts",
        "composition.tests"
    ],

    description='`django-composition` provides the abstract way to denormalize data from your models in simple declarative way through special generic model field called `CompositionField`',
    long_description=get_description(),

    classifiers=[
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
    ]
)
