#!/usr/bin/env python
# *_* coding=utf-8 *_*

import paramiko

hostname_list = ['192.168.1.2', '192.162.1.3']
username = 'admin'
password = 'yourpassword'
port = 22


hostname_list = []

def get_hosts(h_file):
    with open(h_file) as f:
        for l in f.readlines():
            hostname_list.append(l.strip())


def send_file():
    ''' send (or fetch) a file to (or from) a remote linux machine '''
    src_1 = 'ssh_cmd.py'
    dst_1 = '/tmp/ssh_cmd.py'
    put_files = [(src_1, dst_1)]
    for h in hostname_list:
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy)
            print('connecting: %s' % h)
            client.connect(h, port=port, username=username, password=password,
                           timeout=5)
            sftp = client.open_sftp()
            for p in put_files:
                print('src file: %s , dst file: %s' % (p[0], p[1]))
                sftp.put(p[0], p[1])
        except Exception as e:
            print(e)
        finally:
            sftp.close()
            client.close()


if __name__ == '__main__':
    host_file = 'temp_test_ips'
    get_hosts(host_file)
    send_file()
