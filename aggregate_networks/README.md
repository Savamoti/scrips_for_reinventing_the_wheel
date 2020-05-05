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
