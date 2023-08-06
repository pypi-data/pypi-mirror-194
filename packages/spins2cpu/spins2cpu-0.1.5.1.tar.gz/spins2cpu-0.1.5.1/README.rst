.. image:: https://img.shields.io/pypi/v/spins2cpu.svg
   :target: https://pypi.org/project/spins2cpu/

.. image:: https://img.shields.io/pypi/pyversions/spins2cpu.svg
   :target: https://pypi.org/project/spins2cpu/

spins2cpu
=========

spins2cpu: A Monte Carlo Simulation Code for the Phase Transition in 2D/3D Materials

* To execute ``spins2cpu -h`` for the parameters to use.
* Usage Example::

    spins2cpu -h
    spins2cpu -c square -n 4 -x 200 -y 200 -e 200 -w 1000 -t 35 -r
    spins2cpu -x 200 -y 200 -t 0 32 4 33 40 1 40.2 45 0.2 46 55 1 -e 200 -w 1000 -r
    spins2cpu -x 200 -y 200 -c honeycomb -i afm1 -p -1 -t 0 16 2 16 20 0.4 21 25 -r -e 100 -w 1500

