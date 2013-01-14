webserver-monitor
==================

Very simple monitoring utility, that monitors the ``Apache`` and ``wsgi`` applications running. Measures a few of the main resources and characteristics, like memory, cpu usage, number of threads.

It is `curses <http://docs.python.org/library/curses.html>`_ based, and uses the `psutil <http://code.google.com/p/psutil/>`_ module.

The repository includes a ``buildout.cfg`` file, so that the application can be built as a standalone script, and run from the console.

