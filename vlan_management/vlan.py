#!/usr/bin/env python3.7
"""
The script is needed to interact with iproute2, in particular - for vlan management,
creeate, delete, etc

Requirements:
sudo apt-get install python3.7

usage in help:
./vlan.py -h

Put script in ~/.bash_aliases
alias vlan='/home/username/sciprts/./vlan.py'

"""
import subprocess
import argparse


def create_vlan(args):
    """
    create VLAN interface and assign IP

    expect: 3 rows
        ethernet-interface vlan-id ip-with-mask
    return: None or row
        row-from-"ip -4 -br addr"
    """
    # if VLAN interface already exist, return row
    vlan_exist = subprocess.run('ip -4 -br addr', shell=True, stdout=subprocess.PIPE,
        encoding='utf-8')
    for i in vlan_exist.stdout.split('\n'):
        if 'vlan'+args.vlan_id in i:
            print('interface already exist:'.format(args.vlan_id))
            return i
    # create interface
    subprocess.run('sudo ip link add link {} vlan{} type vlan id {}'.format(
        args.interface, args.vlan_id, args.vlan_id), shell=True, stdout=subprocess.DEVNULL)
    # assign IP to VLAN interface
    subprocess.run('sudo ip addr add {} dev vlan{}'. format(args.ip, args.vlan_id),
        shell=True, stdout=subprocess.DEVNULL)
    # up interface
    subprocess.run('sudo ip link set vlan{} up'. format(args.vlan_id),
        shell=True, stdout=subprocess.DEVNULL)


def add_ip(args):
    """
    Assign IP to VLAN interface

    expect: 2 rows
        ip-with-mask vlan-id
    return: None
    """
    subprocess.run('sudo ip addr add {} dev vlan{}'. format(args.ip, args.vlan_id),
        shell=True, stdout=subprocess.DEVNULL)


def delete_ip(args):
    """
    delete IP from VLAN interface

    expect: 2 rows
        ip-with-mask vlan-id
    return: None
    """
    subprocess.run('sudo ip addr del {} dev vlan{}'. format(args.ip, args.vlan_id),
        shell=True, stdout=subprocess.DEVNULL)


def delete_vlan(args):
    """
    Delete interface

    expect: row
        vlan-id
    return: None
    """
    subprocess.run('sudo ip link delete vlan{}'. format(args.vlan_id),
        shell=True, stdout=subprocess.DEVNULL)


if __name__ == "__main__":
    # create parser and subparser
    parser = argparse.ArgumentParser(description='VLAN management')
    subparsers = parser.add_subparsers(title='commands', help='description')

    # subparser for 'create' command
    create_parser = subparsers.add_parser('create', help='create new VLAN')
    create_parser.add_argument('interface', help='ethernet interface: enp3s0'
        'or enp4s0')
    create_parser.add_argument('vlan_id', help='VLAN ID')
    create_parser.add_argument('ip', help='IP with subnet, for example:'
        '192.168.0.254/24')
    # run the function, if arguments a given
    create_parser.set_defaults(func=create_vlan)

    # subparser for 'add' command
    add_parser = subparsers.add_parser('add', help='add IP to VLAN interface')
    add_parser.add_argument('ip', help='IP subnet, for example: 192.168.0.254/24')
    add_parser.add_argument('vlan_id', help='VLAN ID')
    # run the function, if arguments a given
    add_parser.set_defaults(func=add_ip)

    # subparser for 'delete ip' command
    flush_parser = subparsers.add_parser('release', help='delete IP from VLAN interface')
    flush_parser.add_argument('ip', help='IP subnet, for example: 192.168.0.254/24')
    flush_parser.add_argument('vlan_id', help='VLAN ID')
    # run the function, if arguments a given
    flush_parser.set_defaults(func=delete_ip)

    # subparser for 'delete' command
    delete_parser = subparsers.add_parser('delete', help='delete VLAN interface')
    delete_parser.add_argument('vlan_id', help='VLAN ID')
    # run the function, if arguments a given
    delete_parser.set_defaults(func=delete_vlan)

    args = parser.parse_args()
    args.func(args)
    