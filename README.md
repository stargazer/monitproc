webserver-monitor
==================

Very simple monitoring utility, that monitors the ``Apache`` and ``wsgi`` applications running. Measures a few of the main resources and characteristics, like memory, cpu usage, number of threads.

It is `curses <http://docs.python.org/library/curses.html>`_ based, and uses the `psutil <http://code.google.com/p/psutil/>`_ module.

The repository includes a ``buildout.cfg`` file, so that the application can be built as a standalone script, and run from the console.


TODO
-----
1. Rewrite the whole ``metrics.py`` and ``presentation.py`` modules
2. Make sure to understand the metrics that I take
3. Are there more useful measurements to take?
4. Make it more flexible, in the sense that different kinds of processes can be measured... based on name, pid, etc
