#!/usr/bin/env python3
"""
The script converts the MAC address in hexadecimal / bit reversed / dot notation format
and finds the vendor of this MAC address.

requirements:
python3.6 >=
python3.6 -m pip install requests

for convenient use is recommended to do:
nano ~/.bash_aliases
alias mac='~/path/to/the/script/mac.py'
exec bash

structure:
$ tree
.
├── mac.py
└── source
    └── oui.txt

1 directory, 2 files

usage:
$ ./mac.py e0:3f:49:b5:3e:31
UPPER: 
 Hexadecimal:  E0:3F:49:B5:3E:31 
 Bit-reversed: E0-3F-49-B5-3E-31 
 Dot Notation: E03F.49B5.3E31
lower: 
 Hexadecimal:  e0:3f:49:b5:3e:31 
 Bit-reversed: e0-3f-49-b5-3e-31 
 Dot Notation: e03f.49b5.3e31

 ASUSTek COMPUTER INC. 

$ ./mac.py --update
Downloading a file from: http://standards-oui.ieee.org/oui.txt ...
Success.
File /source/oui.txt is outdated, updating...
Success, /source/oui.txt is updated. Run script again.


"""
import argparse
import os

import requests


def convert_mac(mac):
    """
    expect: string
        mac-address
    return: string
        converted mac-address(first 24 bits)
    """
    mac = ''.join(mac).replace(':', '').replace('.', '').replace('-', '')
    # only the first 24 bits are needed to search for a vendor
    textmac = mac[0:6].upper()
    mac = mac.upper()
    print('UPPER:',
        '\n', 'Hexadecimal: ', mac[0:2] + ':' + mac[2:4] + ':' + mac[4:6] + ':' +
        mac[6:8] + ':' + mac[8:10] + ':' + mac[10:12],
        '\n', 'Bit-reversed:', mac[0:2] + '-' + mac[2:4] + '-' + mac[4:6] + '-' + 
        mac[6:8] + '-' + mac[8:10] + '-' + mac[10:12],
        '\n', 'Dot Notation:', mac[0:4] + '.' + mac[4:8] + '.' + mac[8:12])
    mac = mac.lower()
    print('lower:',
        '\n', 'Hexadecimal: ', mac[0:2] + ':' + mac[2:4] + ':' + mac[4:6] + ':' +
        mac[6:8] + ':' + mac[8:10] + ':' + mac[10:12],
        '\n', 'Bit-reversed:', mac[0:2] + '-' + mac[2:4] + '-' + mac[4:6] + '-' + 
        mac[6:8] + '-' + mac[8:10] + '-' + mac[10:12],
        '\n', 'Dot Notation:', mac[0:4] + '.' + mac[4:8] + '.' + mac[8:12])
    return textmac


def find_in_file(mac):
    with open(path, 'r') as file:
        for line in file:
            if mac in line:
                _,_,_,*last = line.split()
                last = ' '.join(last)
                print('\n',last,'\n')
                return True
        print(f"\nCan't find the vendor for this MAC address. Try to update source file {path_mac_file}.\n"
            "Run:\n"
            "mac --update")
        

def update_file(url):
    print("Download a file from:", url, '...')
    new_source = requests.get(url)
    print("Success.")
    with open(path, 'rb') as file:
        old_source = file.read()
    if new_source.content == old_source:
        print(f"File {path_mac_file} is up-to-date.")
    else:
        print(f"File {path_mac_file} is outdated, updating...")
        with open(path, 'wb') as file:
            file.write(new_source.content)
            print(f"Success, {path_mac_file} is updated. Run script again.")


if __name__ == "__main__":
    # SETTINGS
    # link to mac-address database
    url = 'http://standards-oui.ieee.org/oui.txt'
    # path to mac source file
    path_mac_file = 'source/oui.txt'

    parser = argparse.ArgumentParser(description='MAC-address lookup.')
    parser.add_argument('mac', nargs='?', action='store', help='mac-address')
    parser.add_argument('--update', action='store_true', help='update a mac source file')
    args = parser.parse_args()

    path = os.path.join(os.getcwd(), os.path.dirname(__file__), path_mac_file)

    if args.mac:
        mac = convert_mac(args.mac)
        find_in_file(mac)
    elif args.update:
        update_file(url)
    else:
        parser.print_usage()
        print("One of this arguments is required: mac or --update.")
