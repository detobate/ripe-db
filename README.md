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

  -4          IPv4 inetnum objects.
  -6          IPv6 inet6num objects.

Status:
  Select which inet[6]num objects to display. At least one required.

  -A          Assigned inet[6]num objects.
  -a          Allocated inet[6]num objects.
  -s          Sub-Allocated inet[6]num objects.
  -l          Legacy inet[6]num objects.
```