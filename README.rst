.. image:: https://img.shields.io/pypi/v/singledispatch.svg
   :target: https://pypi.org/project/singledispatch

.. image:: https://img.shields.io/pypi/pyversions/singledispatch.svg

.. image:: https://github.com/jaraco/singledispatch/actions/workflows/main.yml/badge.svg
   :target: https://github.com/jaraco/singledispatch/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. image:: https://readthedocs.org/projects/singledispatch/badge/?version=latest
   :target: https://singledispatch.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/badge/skeleton-2025-informational
   :target: https://blog.jaraco.com/skeleton

.. image:: https://tidelift.com/badges/package/pypi/singledispatch
   :target: https://tidelift.com/subscription/pkg/pypi-singledispatch?utm_source=pypi-singledispatch&utm_medium=readme

`PEP 443 <http://www.python.org/dev/peps/pep-0443/>`_ proposed to expose
a mechanism in the ``functools`` standard library module in Python 3.4
that provides a simple form of generic programming known as
single-dispatch generic functions.

This library is a backport of this functionality and its evolution.

Refer to the `upstream documentation
<http://docs.python.org/3/library/functools.html#functools.singledispatch>`_
for API guidance. To use the backport, simply use
``from singledispatch import singledispatch, singledispatchmethod`` in place of
``from functools import singledispatch, singledispatchmethod``.


Maintenance
===========

This backport is maintained on Github by Jason R. Coombs, one of the
members of the core CPython team:

* `repository <https://github.com/jaraco/singledispatch>`_

* `issue tracker <https://github.com/jaraco/singledispatch/issues>`_

For Enterprise
==============

Available as part of the Tidelift Subscription.

This project and the maintainers of thousands of other packages are working with Tidelift to deliver one enterprise subscription that covers all of the open source you use.

`Learn more <https://tidelift.com/subscription/pkg/pypi-singledispatch?utm_source=pypi-singledispatch&utm_medium=referral&utm_campaign=github>`_.
