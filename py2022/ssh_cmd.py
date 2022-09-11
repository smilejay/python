#!/usr/bin/python

import paramiko

hostname_list = ['192.168.1.2', '192.162.1.3']
username = 'root'
password = 'yourpassword'
username = 'admin'
password = ''
port = 22


hostname_list = []

def get_hosts(h_file):
    with open(h_file) as f:
        for l in f.readlines():
            hostname_list.append(l.strip())


def exec_cmd(cmd):
    ''' exec a cmd on a remote linux system '''
    for h in hostname_list:
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy)
            print('connecting: %s' % h)
            client.connect(h, port=port, username=username, password=password,
                           timeout=5)
            chan = client.get_transport().open_session()
            print('exec cmd: %s' % cmd)
            chan.exec_command(cmd)
            print('exit code: %d' % chan.recv_exit_status())
            if chan.recv_exit_status() == 0:
                print('%s OK' % h)
            else:
                print('%s Error!' % h)
            print(chan.recv(200).strip())
            # stdin, stdout, stderr = client.exec_command(cmd)
            # print(stdout.read().strip())
            # print(stderr.read().strip())
        except Exception as e:
            print(e)
        finally:
            client.close()


if __name__ == '__main__':
    host_file = 'temp_test_ips'
    get_hosts(host_file)
    cmd = 'uptime'
    cmd = 'echo $(date)>>/tmp/a; sleep 1; uptime; exit 1'
    exec_cmd(cmd)
