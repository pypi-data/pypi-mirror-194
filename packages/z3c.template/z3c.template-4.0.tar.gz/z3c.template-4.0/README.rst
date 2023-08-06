==============
 z3c.template
==============


.. image:: https://img.shields.io/pypi/v/z3c.template.svg
        :target: https://pypi.python.org/pypi/z3c.template/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/z3c.template.svg
        :target: https://pypi.org/project/z3c.template/
        :alt: Supported Python versions

.. image:: https://github.com/zopefoundation/z3c.template/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/zopefoundation/z3c.template/actions/workflows/tests.yml


.. image:: https://coveralls.io/repos/github/zopefoundation/z3c.template/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/z3c.template?branch=master


This package allows you to register templates independently from view code.

In Zope 3, when registering a ``browser:page`` both presentation and computation
are registered together. Unfortunately the registration tangles presentation
and computation so tightly that it is not possible to re-register a different
template depending on context. (You can override the whole registration but
this is not the main point of this package.)

With z3c.template the registration is split up between the view and the
template and allows to differentiate the template based on the skin layer and
the view.

In addition this package lays the foundation to differentiate between
templates that provide specific presentation templates and generic layout
templates.
