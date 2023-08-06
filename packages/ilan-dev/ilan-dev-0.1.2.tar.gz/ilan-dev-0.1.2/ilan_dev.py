import tarfile
from os.path import dirname


__version__ = "0.1.2"


def lcp(a):
    """
    return longest common prefix of iterable of strings,
    or None when iterable is exhausted immediately
    """
    a = list(a)
    if len(a) == 0:
        return None
    first, last = min(a), max(a)
    stop = min(len(first), len(last))
    # find the common prefix between the first and last string
    i = 0
    while i < stop and first[i] == last[i]:
        i += 1
    return first[:i]


def human_bytes(n):
    """
    return size (in bytes) in more human readable form
    """
    if n < 1024:
        return '%d' % n
    k = float(n) / 1024
    if k < 1024:
        return '%dK' % round(k)
    m = k / 1024
    if m < 1024:
        return '%.1fM' % m
    g = m / 1024
    return '%.2fG' % g


def tar_nameset(path):
    with tarfile.open(path) as t:
        return set(m.path for m in t.getmembers())


def tar_get_empty_dirs(path):
    "given a tarball, return set with all empty directories"
    with tarfile.open(path) as t:
        dirs1 = set()  # all directories listed in tarball
        dirs2 = set()  # all directories that contain files
        for m in t.getmembers():
            if m.isdir():
                dirs1.add(m.path)
                continue
            # for each file path, add the directories leading to its path
            p = dirname(m.path)
            while p not in dirs2:
                dirs2.add(p)
                p = dirname(p)

    return dirs1 - dirs2
