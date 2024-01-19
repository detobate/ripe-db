RIPE Database Scripts
========

inetnums.py
-----------

```
 % ./inetnums.py --help
usage: inetnums.py [-h] [-c] [-4] [-6] [-A] [-a] [-s] [-l] <orgID> [<orgID> ...]

Query the RIPE Database for inet[6]num objects

positional arguments:
  <orgID>     LIR Org ID[s]

options:
  -h, --help  show this help message and exit
  -c          Output IPv4 CIDR notation

Address Families:
  Select which address families to display. At least one required.

  -4          IPv4 inetnum objects. [Default: False]
  -6          IPv6 inet6num objects. [Default: False]

Status:
  Select which inet[6]num objects to display. At least one required.

  -A          Assigned inet[6]num objects. [Default: False]
  -a          Allocated inet[6]num objects. [Default: False]
  -s          Sub-Allocated inet[6]num objects. [Default: False]
  -l          Legacy inet[6]num objects. [Default: False]
```