import datetime


def fib1(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib1(n - 1) + fib1(n - 2)


known = {0: 0, 1: 1}


def fib2(n):
    if n in known:
        return known[n]

    res = fib2(n - 1) + fib2(n - 2)
    known[n] = res
    return res


if __name__ == '__main__':
    n = 40
    print(datetime.datetime.now())
    print('fib1(%d)=%d' % (n, fib1(n)))
    print(datetime.datetime.now())
    print('fib2(%d)=%d' % (n, fib2(n)))
    print(datetime.datetime.now())
