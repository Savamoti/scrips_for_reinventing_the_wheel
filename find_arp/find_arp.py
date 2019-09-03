#!/usr/bin/python3.7
"""
The script connects to switch, picks up full arp table.
Depending on what arguments argparse parsed, rows from the arp table will be out to stdout.
+ will find vendor of mac-address

requirements:
    sudo apt-get install python3.7 python3-pip
    pip3 install tabulate
"""

import pexpect
import argparse
from tabulate import tabulate

def get_arp_table():
    """
    The function connects to the switch by telnet and picks up the arp-table

    expect: None
    return: row
        arp-table
    """
    IP = ''
    login = ''
    password = ''
    telnet = pexpect.spawn('telnet {}'.format(IP), timeout=30)
    telnet.expect('Username:')
    telnet.sendline(login)
    telnet.expect('Password:')
    telnet.sendline(password)
    telnet.expect('#')
    telnet.sendline('terminal length 0')
    telnet.expect('#')
    telnet.sendline('show arp')
    telnet.expect('#')
    arp_table = telnet.before.decode('utf-8')
    telnet.close()
    return arp_table


def convert_mac(mac, format):
    """
    The function converts mac address, there is 3 format:
    1 - Bit-reversed: 98-DE-D0-01-04-3D
    2 - Dot Notation: 98DE.D001.043D
    3 - The first 3 bits(need for vendor identification): 98DE

    expect: row | format
        mac-address | 1/2/3
    return: row
        converted mac-address
    """
    mac = ''.join(mac).replace(':', '').replace('.', '').replace('-', '').upper()
    if format == 1:
        mac = mac[0:2] + '-' + mac[2:4] + '-' + mac[4:6] + '-' + mac[6:8] + '-' + mac[8:10] + '-' + mac[10:12]
        return mac
    elif format == 2:
        mac = mac[0:4] + '.' + mac[4:8] + '.' + mac[8:12]
        mac = mac.lower()
        return mac
    elif format == 3:
        mac = mac[0:6]
        return mac
    else:
        pass


def find_in_database(mac):
    """
    The function searches for a vendor by mac.

    expect: row
        for example: 84C9B2
    return: row
        vendor name
    """
    with open('source/oui.txt', 'r') as start:
        for line in start:
            if line.count(mac) == 1:
                _,_,_,*last = line.split()
                last = ' '.join(last)
                return last


def search_mac_in_arp(args):
    """
    Fuction searches a mac-address in the arp table.
    
    expect: row
        mac-address
    return: None

    """
    arp_table = get_arp_table()
    
    mac = convert_mac(args.mac, 2)
    columns = ['IP', 'AGE(min)', 'MAC', 'INTERFACE', 'VENDOR']
    result = []
    for row in arp_table.split('\n'):
        if mac in row:
            lists = []
            _,ip,age,r_mac,_,interface = row.strip().split()
            r_mac = convert_mac(mac, 1)
            vendor = convert_mac(r_mac, 3)
            vendor = find_in_database(vendor)
            r_mac = blue + r_mac + endblue
            lists = [ip, age, r_mac, interface, vendor]
            result.append(lists)
        else:
            pass
    print(tabulate(result, headers=columns))


def search_ip_in_arp(args):
    """

    """
    arp_table = get_arp_table()
    
    columns = ['IP', 'AGE(min)', 'MAC', 'INTERFACE', 'VENDOR']
    result = []
    for row in arp_table.split('\n'):
        if args.ip in row:
            lists = []
            _,ip,age,mac,_,interface = row.strip().split()
            r_mac = convert_mac(mac, 1)
            ip = blue + ip + endblue
            vendor = convert_mac(r_mac, 3)
            vendor = find_in_database(vendor)
            lists = [ip, age, r_mac, interface, vendor]
            result.append(lists)
        else:
            pass
    print(tabulate(result, headers=columns))


if __name__ == "__main__":
    # font-color
    blue = """\033[96m"""
    endblue = """\033[0m"""
    # create parser and subparser
    parser = argparse.ArgumentParser(description='Search arp record')
    subparsers = parser.add_subparsers(title='commands', help='description')

    # subparser for 'mac' command
    mac_parser = subparsers.add_parser('mac', help='search by mac-address')
    mac_parser.add_argument('mac', help='mac-address')
    # run the function, if arguments a given
    mac_parser.set_defaults(func=search_mac_in_arp)

    # subparser for 'ip' command
    ip_parser = subparsers.add_parser('ip', help='delete VLAN interface')
    ip_parser.add_argument('ip', help='IP-address')
    # run the function, if arguments a given
    ip_parser.set_defaults(func=search_ip_in_arp)

    # if args is empty, print usage text
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        args.func(args)


"""
It looks like this:

13:12 $ ./find_arp.py mac e0:3f:49:b5:3e:31
IP                AGE(min)  MAC                INTERFACE    VENDOR
--------------  ----------  -----------------  -----------  ---------------------
192.168.101.10          26  E0-3F-49-B5-3E-31  Vlan11       ASUSTek COMPUTER INC.

13:19 $ ./find_arp.py ip 192.168.193.2
IP               AGE(min)  MAC                INTERFACE    VENDOR
-------------  ----------  -----------------  -----------  --------------------
192.168.193.2           4  00-AD-24-D1-BD-19  Vlan13       D-Link International
"""