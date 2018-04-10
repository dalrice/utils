import itertools

def igroup(iterable, n):
    # igroup('ABCDEFG', 2) --> iter[(A, B), (C,D), (E, F), (G,)]
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk: return
       yield chunk
