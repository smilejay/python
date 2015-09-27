'''
calculate how many zero(0)s in the end of n!.
'''


def zero_cnt_of_factorial(num=50):
    count = 0
    delta = 5
    m = 5
    while m <= num:
        count += 1
        m1 = m / delta
        while m1 > 0:
            if m1 % delta == 0:
                count += 1
            m1 = m1 / delta
        m += 5
    return count

if __name__ == '__main__':
    n = int(raw_input('Enter a number: '))
    print "%d! has %d zeros in the end." % (n, zero_cnt_of_factorial(n))
