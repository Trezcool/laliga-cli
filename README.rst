======
README
======

A simple command-line application that will calculate the ranking table for a soccer league.


Setup and configuration
=======================

Create a new Python3 virtualenv and install the package:
``pip install -e .``


Running the App
===============

To run the app, just do:
``laliga``
and follow the instructions.

The fixture result format is: ``Barcelona 3, Real Madrid 1``.
If results are in a file, there should be one result per line!


Testing
=======

Install required packages for testing if they ain't yet installed:
``pip install -r requirements-tests.txt``

To test the app, just do:
``pytest``
