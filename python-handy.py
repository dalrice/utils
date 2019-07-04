import itertools

def igroup(iterable, n):
    # igroup('ABCDEFG', 2) --> iter[(A, B), (C,D), (E, F), (G,)]
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk: return
       yield chunk
    
def run_parallel(*fns):
    def helper():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(fns)) as e:
            fs = [e.submit(fn) for fn in fns]
            for f in fs:
                yield f.result()
    return tuple(helper())
