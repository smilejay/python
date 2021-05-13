import os
import gc
import time
import psutil


def print_memory_info():
    pid = os.getpid()
    p = psutil.Process(pid)

    info = p.memory_full_info()
    MB = 1024 * 1024
    memory = info.uss / MB
    print('used %d MB' % memory)

def test_func():
    print("test start")
    print_memory_info()
    length = 1000 * 1000
    list = [i for i in range(length)]
    print_memory_info()

def test1_func():
    print("test1 start")
    print_memory_info()
    length = 1000 * 1000
    list_a = [i for i in range(length)]
    list_b = [i for i in range(length)]
    list_a.append(list_b)
    list_b.append(list_a)
    print_memory_info()
    return list


test_func()
print_memory_info()
test1_func()
print_memory_info()
time.sleep(10)
print_memory_info()
gc.collect()
print_memory_info()
