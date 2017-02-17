from multiprocessing import Pool
import os
import time
import random


def exponent(name, x, y):
    print 'Run task %s (%s)...' % (name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print 'Task %s runs %0.2f seconds.' % (name, (end - start))
    return x**y


if __name__ == '__main__':
    print 'Parent process %s.' % os.getpid()
    p = Pool(4)
    results = [p.apply_async(exponent, args=(i, x, y))
               for (i, x, y) in zip(range(10), range(10), range(10))]
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
    output = [r.get() for r in results]
    print output
