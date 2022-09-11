# *_* coding=utf-8 *_*

import time
import functools


# 装饰器 用于打印函数执行耗时  性能分析很有用
# 这是为python2 写的； python3中 不要使用time.clock()了
# DeprecationWarning: time.clock has been deprecated in Python 3.3 and will be removed from Python 3.8: use time.perf_counter or time.process_time instead
def time_it(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        # start = time.clock()
        start = time.time()
        func(*args, **kwargs)
        # end = time.clock()
        end = time.time()
        print("function %s() costs %s second(s)" % (func.__name__, end - start))
    return _wrapper


@time_it
def test1(x, y):
    time.sleep(1)
    return x + y


@time_it
def test2(x, y):
    time.sleep(3)
    return x + y

if __name__ == '__main__':
    test1(3, 5)
    test2(3, 5)
