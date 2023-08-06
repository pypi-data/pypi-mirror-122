=============================
Django Clear S2S
=============================

.. image:: https://badge.fury.io/py/Django-clear-s2s.svg
    :target: https://badge.fury.io/py/Django-clear-s2s

.. image:: https://travis-ci.org/sal-git/Django-clear-s2s.svg?branch=master
    :target: https://travis-ci.org/sal-git/Django-clear-s2s

.. image:: https://codecov.io/gh/sal-git/Django-clear-s2s/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/sal-git/Django-clear-s2s

Your project description goes here

Documentation
-------------

The full documentation is at https://Django-clear-s2s.readthedocs.io.

Quickstart
----------

Install Django Clear S2S::

    pip install Django-clear-s2s

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_clear_s2s.apps.DjangoClearS2sConfig',
        ...
    )

Add Django Clear S2S's URL patterns:

.. code-block:: python

    from django_clear_s2s import urls as django_clear_s2s_urls


    urlpatterns = [
        ...
        url(r'^', include(django_clear_s2s_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
