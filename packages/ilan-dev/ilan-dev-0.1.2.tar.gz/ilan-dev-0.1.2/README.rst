Ilan's dev tools
================

A collection of very small tools I've been using for many many years:

.. code-block:: shell-session

    $ pip install ilan-dev
    $ cleanup -h
    Usage: cleanup [options] FILE [FILE ...]

    Cleanup whitespace in FILE, that is: remove carriage returns; remove excess
    whitespace at the end of each line; expand tabs (to 8 spaces), but not a
    Makefile; make sure file has a newline at the end

    Options:
      -h, --help     show this help message and exit
      --ascii-only   allow only ASCII bytes (removes others)
      -n, --dry-run  show which files would have been rewritten
      -r, --recur    cleanup recursively
    $ tarinfo -h
    Usage: tarinfo [options] TAR [TAR ...]

    display useful information about tar files

    Options:
      -h, --help  show this help message and exit
      --cext      list Python C extension imports
      --common    list archive name common in all tarballs
      --diff      show difference of two tarballs (archive names only)
      --lcp       show the longest common prefix of all archive names
      --repack    repack tarballs
      --size      list file sizes of all archives (sorted by size)

