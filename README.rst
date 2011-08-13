webserver-monitor
==================

Very simple monitoring utility, that monitors the ``Apache`` and ``wsgi`` applications running on a server. Cool for Django projects.


It monitors a few of the main resources and characteristics, like memory, cpu usage, number of threads.

It is `curses <http://docs.python.org/library/curses.html>`_ based, and uses the `psutil <http://code.google.com/p/psutil/>`_ module.

The code is ugly, but still works nicely :) I hope I will re-write it soon in a much better way.

``How to use:``

	*	Checkout repository
	*	If you want to use the package as is:

		* ``python bootstrap.py``
		*	``bin/buildout``		
		* Script ``bin/monitor`` should be available in the local folder

	*	If you want to integrate it on a buildout:

		* Use ``mr.developer`` to checkout the code and develop the egg.
		* ``bin/buildout``
		* Script ``bin/monitor`` should be available in your project's folder.
