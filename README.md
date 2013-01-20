monitproc
==================

Very simple monitoring utility, that monitors any processes you'd like. It measures a few of the main resources and characteristics, like memory, cpu usage, number of threads.

It's [curses](http://docs.python.org/library/curses.html) based, and uses the [psutil](http://code.google.com/p/psutil/>) module as a backend.

The repository includes a ``buildout.cfg`` file, so that the application can be built as a standalone script, and run from the console.

How to use
--------------
Install by:

    git clone git@github.com:stargazer/monitproc.git
    cd monitproc
    python bootstrap.py -d
    bin/buildout

Now you can use the tool by running:
    
    bin/monitproc <proc1> <proc2> <...>


TODO
-----
1. Rewrite the whole ``metrics.py`` and ``presentation.py`` modules
2. Document the measurements that I take
3. Are there more useful measurements to take?
4. Make it more flexible, in the sense that different kinds of processes can be measured... based on name, pid, etc
5. On top of the screen, print system information... CPU freq, total memory, swap space, etc
