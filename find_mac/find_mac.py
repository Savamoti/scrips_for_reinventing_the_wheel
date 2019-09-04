#!/usr/bin/env python3
"""
Script converts mac-address and finds verdor.
"""
import argparse


def convert_mac(mac):
    """
    expect: string
        mac-address
    return: string
        converted mac-address
    """
    mac = ''.join(mac).replace(':', '').replace('.', '').replace('-', '')
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


def find_in_database(mac):
    with open('source/oui.txt', 'r') as start:
        for line in start:
            if line.count(mac) == 1:
                _,_,_,*last = line.split()
                last = ' '.join(last)
                print('\n',last,'\n')
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MAC-addresse lookup')
    parser.add_argument('mac', action='store', help='mac-address')
    args = parser.parse_args()
    mac = convert_mac(args.mac)
    find_in_database(mac)


"""
17:44 $ ./test.py 00:25:22:32:3d:3e
UPPER: 
 Hexadecimal:  00:25:22:32:3D:3E 
 Bit-reversed: 00-25-22-32-3D-3E 
 Dot Notation: 0025.2232.3D3E
lower: 
 Hexadecimal:  00:25:22:32:3d:3e 
 Bit-reversed: 00-25-22-32-3d-3e 
 Dot Notation: 0025.2232.3d3e

 ASRock Incorporation 

"""