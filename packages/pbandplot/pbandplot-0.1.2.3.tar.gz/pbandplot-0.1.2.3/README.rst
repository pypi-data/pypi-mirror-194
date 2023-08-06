.. image:: https://img.shields.io/pypi/v/pbandplot.svg
   :target: https://pypi.org/project/pbandplot/

.. image:: https://img.shields.io/pypi/pyversions/pbandplot.svg
   :target: https://pypi.org/project/pbandplot/

pbandplot
=========

pbandplot: Plot the phonon band structure plot from phonopy result.

* To execute ``pbandplot -h`` for the parameters to use.
* Example::

    pbandplot -i band.dat -o pband.png -l g m k g -d projected_dos.dat
    pbandplot -b 23 100 -l g m k g -y -2 110

