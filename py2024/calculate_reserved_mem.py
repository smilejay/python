#!/usr/bin/python3

import re
import sys
from subprocess import Popen, PIPE, STDOUT


def shell_rc_and_output(cmd):
    ''' execute a shell command and get its return code and output (stdout/stderr) '''
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    out = p.communicate()[0]
    rc = p.returncode
    if isinstance(out, bytes):
        # out is a string
        out = out.decode()
    return rc, str(out)


def parse_memory_line(line):
    """
    解析单行内存映射信息，并返回内存区域的起始和结束地址。
    """
    pattern = '.+\[mem (.+)-(.+)\].+'
    match = re.search(pattern, line)
    # print(match)
    if match:
        start = match.group(1)
        end = match.group(2)
        # print(match.group(1))
        # print(match.group(2))
        start = int(start, 16)
        end = int(end, 16)
        return start, end


def calculate_reserved_memory(lines):
    """
    计算所有保留内存区域的总大小。
    """
    total_reserved_memory = 0
    for line in lines:
        if 'mem' in line and 'reserved' in line:
            start, end = parse_memory_line(line)
            # 计算内存区域的大小，并考虑包含结束地址
            size = end - start + 1
            total_reserved_memory += size
    return total_reserved_memory


def calculate_memory(lines):
    """
    计算所有内存区域的总大小。
    """
    total_memory = 0
    for line in lines:
        if 'mem' in line:
            start, end = parse_memory_line(line)
            # 计算内存区域的大小，并考虑包含结束地址
            size = end - start + 1
            total_memory += size
    return total_memory


def get_e820_mem_map():
    """"
    根据 dmesg -T 命令查看 e820表的信息, 返回一个列表。
    """
    # 返回如下这样格式的列表 (放在这里仅供代码调试用)
    # memory_map = [
    #     "BIOS-e820: [mem 0x0000000000000000-0x000000000009ffff] usable",
    #     "BIOS-e820: [mem 0x0000000000100000-0x000000005ad0efff] usable",
    #     "BIOS-e820: [mem 0x000000005ad0f000-0x0000000060377fff] reserved",
    #     "BIOS-e820: [mem 0x0000000060378000-0x000000007fffefff] usable",
    #     "BIOS-e820: [mem 0x000000007ffff000-0x000000007fffffff] reserved",
    #     "BIOS-e820: [mem 0x0000000080000000-0x00000000bf8eefff] usable",
    #     "BIOS-e820: [mem 0x00000000bf8ef000-0x00000000bfb6efff] reserved",
    #     "BIOS-e820: [mem 0x00000000bfb6f000-0x00000000bfb7efff] ACPI data",
    #     "BIOS-e820: [mem 0x00000000bfb7f000-0x00000000bfbfefff] ACPI NVS",
    #     "BIOS-e820: [mem 0x00000000bfbff000-0x00000000bff7bfff] usable",
    #     "BIOS-e820: [mem 0x00000000bff7c000-0x00000000bfffffff] reserved",
    #     "BIOS-e820: [mem 0x0000000100000000-0x000000081fffffff] usable",
    #     "BIOS-e820: [mem 0x0000000820000000-0x000000083fffffff] reserved"
    # ]
    # return memory_map
    cmd = "dmesg -T | grep -Eio ' (bios-e820:.*mem .*)'"
    rc, out = shell_rc_and_output(cmd)
    if rc != 0:
        print("Error! failed to run cmd: {}".format(cmd))
        sys.exit(1)
    else:
        memory_map = out.split('\n')
        return memory_map


def print_reserved_ratio(total, reserved):
    """
    计算内存被reserved的比例, 并打印百分比
    """
    ratio = reserved / total
    percentage = ratio * 100
    print("memory reserved percentage: {:.2f}%".format(percentage))


if __name__ == '__main__':
    # 获取BIOS-e820内存映射信息
    mem_map = get_e820_mem_map()
    # 计算总内存大小
    total_memory = calculate_memory(mem_map)
    total_mem_mb = total_memory / 1024 / 1024
    print("Total memory: {:.0f} MB".format(total_mem_mb))
    # 计算保留的内存大小
    reserved_memory = calculate_reserved_memory(mem_map)
    res_mem_mb = reserved_memory / 1024 / 1024
    print("Total reserved memory: {:.0f} MB".format(res_mem_mb))
    print_reserved_ratio(total_mem_mb, res_mem_mb)
