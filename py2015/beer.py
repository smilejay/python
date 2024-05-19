#!/usr/bin/python3
'''
calculate how many bottles of beer you can drink.
1. money: n RMB (e.g. n=10)
2. price: 2 RMB / bottle
3. 3 empty bottles --> 1 bottle of beer
可以最多向商店借1个空瓶, 但需要兑换喝完后将1个空瓶还回。
2024年update: a. 增加了向商店借空瓶的说明  b. 使用python3而不是python2
'''


def bottles_cnt_beer(money=10):
    '''
    计算能够喝到多少瓶啤酒。
    供参考答案如下：
    10 -> 7
    100 -> 75
    1234 -> 925
    12345 -> 9258
    '''
    price = 2
    m = 3   # m empty bottles --> 1 bottle of beer
    count = int(money / price)
    empty_cnt = int(money / price)
    while empty_cnt >= m:
        count += int(empty_cnt / m)
        empty_cnt = int(empty_cnt / m) + int(empty_cnt % m)
    # borrow 1 empt bottle from the shop; drink; return 1 empty bottle to the shop.
    if empty_cnt == (m - 1):
        count += 1
    return count


if __name__ == '__main__':
    n = 10
    print("money n={}, you can drink {} bottles of beer.".format(n, bottles_cnt_beer(n)))
    n = 100
    print("money n={}, you can drink {} bottles of beer.".format(n, bottles_cnt_beer(n)))
    n = 1234
    print("money n={}, you can drink {} bottles of beer.".format(n, bottles_cnt_beer(n)))
    n = int(input('Enter a number: '))
    print("money n={}, you can drink {} bottles of beer.".format(n, bottles_cnt_beer(n)))
