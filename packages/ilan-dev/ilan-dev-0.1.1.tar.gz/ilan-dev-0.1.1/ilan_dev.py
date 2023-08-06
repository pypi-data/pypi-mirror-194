import os
import tarfile


__version__ = "0.1.1"


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


def tar_repack(path, remove=None):
    assert path.endswith(('.tgz', '.tar.gz'))

    tmp_path = path + '.tmp'
    os.replace(path, tmp_path)

    # s -> t
    with tarfile.open(tmp_path) as s:
        with tarfile.open(path, 'w:gz') as t:
            for member in s.getmembers():
                if member.isdir():
                    continue
                path = member.path
                if remove is not None and path in remove:
                    continue
                t.addfile(member, s.extractfile(path))

    os.unlink(tmp_path)
