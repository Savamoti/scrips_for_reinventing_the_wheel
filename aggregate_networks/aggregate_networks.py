#!/usr/bin/env python3
"""
# Aggregate_networks.py

### What is this?
The script aggregate IPv4/IPv6 networks.

From this:
`192.168.1.0/25 192.168.1.128/25`

To this:
`192.168.1.0/24`

### Usage:

```
$ ./aggregate_networks.py '185.32.248.0/22
> 87.240.128.0/18
> 93.186.224.0/21
> 93.186.232.0/21
> 95.142.192.0/20
> 95.142.192.0/21
> 95.142.206.0/24
> 95.213.0.0/18
> 95.213.64.0/18
> 2a00:bdc0:1000::/36
> 2a00:bdc0::/36
> 2a00:bdc0:e006::/48'

Aggregated IP networks:
87.240.128.0/18
93.186.224.0/20
95.142.192.0/20
95.213.0.0/17
185.32.248.0/22
2a00:bdc0::/35
2a00:bdc0:e006::/48
```

### Requirements:
* python3 >=
* pip3 install netaddr

"""

import argparse
import sys

try:
    from netaddr import IPNetwork, cidr_merge
except ModuleNotFoundError:
    print("ERROR: netaddr library not installed.\n"
        "Install it with:\n\n"
        "pip3 install netaddr\n"
        )
    sys.exit()


def main(network_list):
    """
    expect: list
        list of IP networks
    return: list
        aggregated IP networks
    """
    try:
        network_list = [IPNetwork(net) for net in network_list.strip().split()]
        network_list = cidr_merge(network_list)
        return network_list
    except Exception as error:
        print(error)
        return False


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description='IPv4/IPv6 network aggregator.')
    parser.add_argument('ip_networks',
        help="Format: '192.168.1.0/25 192.168.1.128/25'")
    args = parser.parse_args()

    # main
    network_list = main(args.ip_networks)
    if network_list:
        print('\nAggregated IP networks:')
        for network in network_list:
            print(network)