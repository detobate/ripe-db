#!/usr/bin/env python3
import requests
import ipaddress
import argparse


def net4_to_cidr(net):
    """ Converts a network range such as 10.0.0.0 - 10.255.255.255 in to CIDR notation"""

    try:
        start, end = net.split(' - ')
    except ValueError:
        print(f'ERROR: {net} is not in "10.0.0.0 - 10.255.255.255" range format')
        return None

    cidr = None

    startip = ipaddress.IPv4Address(start)

    # inetnum assignments exclude the broadcast address as they need to be smaller than the parent allocation
    # So we'll infer the end is the broadcast
    if end[-3:] == '254':
        end = end[:-3] + '255'
    endip = ipaddress.IPv4Address(end)

    try:
        cidr = [ipaddr for ipaddr in ipaddress.summarize_address_range(startip, endip)]
    except TypeError:
        print(f'Error: net:{net} start:{startip} end:{endip}')

    return cidr


def parse_inetnum_results(results, cidr, assigned, allocated, legacy, sub_allocated):

    if cidr:
        print('cidr,netname,status,mnt-by')
    else:
        print('inetnum,netname,status,mnt-by')
    try:
        for obj in results['objects']['object']:
            mnt_by = []
            for attr in obj['attributes']['attribute']:
                if attr['name'] == 'inetnum' or attr['name'] == 'inet6num':
                    inetnum = attr['value']
                elif attr['name'] == 'netname':
                    netname = attr['value']
                elif attr['name'] == 'status':
                    status = attr['value']
                elif attr['name'] == 'mnt-by':
                    mnt_by.append(attr['value'])

            if ((status in ('ALLOCATED PA', 'ALLOCATED UNSPECIFIED') and allocated) or
                    (status == 'SUB-ALLOCATED PA' and sub_allocated) or
                    (status in ('ASSIGNED PA', 'ASSIGNED PI') and assigned) or
                    (status == 'LEGACY' and legacy)):
                try:
                    if cidr:
                        c = net4_to_cidr(inetnum)
                        print(f'{c[0]},{netname},{status},{mnt_by}')
                    else:
                        print(f'{inetnum},{netname},{status},{mnt_by}')
                except NameError:
                    pass

    except KeyError:
        print(results['errormessages'])


def parse_inet6num_results(results, assigned, allocated, legacy, sub_allocated):

    print('inet6num,netname,status,mnt-by')
    try:
        for obj in results['objects']['object']:
            mnt_by = []
            for attr in obj['attributes']['attribute']:
                if attr['name'] == 'inet6num':
                    inet6num = attr['value']
                elif attr['name'] == 'netname':
                    netname = attr['value']
                elif attr['name'] == 'status':
                    status = attr['value']
                elif attr['name'] == 'mnt-by':
                    mnt_by.append(attr['value'])

            if ((status == 'ALLOCATED-BY-RIR' and allocated) or
                    (status == 'ALLOCATED-BY-LIR' and sub_allocated) or
                    (status in ('ASSIGNED', 'AGGREGATED-BY-LIR') and assigned) or
                    (status == 'LEGACY' and legacy)):
                print(f'{inet6num},{netname},{status},{mnt_by}')

    except KeyError:
        print(results['errormessages'])


def main():

    parser = argparse.ArgumentParser(description='Query the RIPE Database for inet[6]num objects')
    parser.add_argument('orgs', metavar='<orgID>', help='LIR Org ID[s]', action='append', nargs='+')
    parser.add_argument('-c', action='store_true', default=False, help='Output IPv4 CIDR notation')
    address_family = parser.add_argument_group('Address Families', 'Select which address families to display. '
                                                                   'At least one required.')
    address_family.add_argument('-4', dest='v4', action='store_true',
                                default=False, help='IPv4 inetnum objects.')
    address_family.add_argument('-6', dest='v6', action='store_true',
                                default=False, help='IPv6 inet6num objects.')
    status = parser.add_argument_group('Status', 'Select which inet[6]num objects to display. '
                                                 'At least one required.')
    status.add_argument('-A', action='store_true', default=False,
                        help='Assigned inet[6]num objects.')
    status.add_argument('-a', action='store_true', default=False,
                        help='Allocated inet[6]num objects.')
    status.add_argument('-s', action='store_true', default=False,
                        help='Sub-Allocated inet[6]num objects.')
    status.add_argument('-l', action='store_true', default=False,
                        help='Legacy inet[6]num objects.')
    args = parser.parse_args()

    if not (args.A or args.a or args.l):
        parser.error('At least one of -A -a -l required')

    if not (args.v4 or args.v6):
        parser.error('At least one of -6 -4 required')

    cidr = args.c
    assigned = args.A
    allocated = args.a
    legacy = args.l
    sub_allocated = args.s

    header = {'Accept': 'application/json'}
    base_url = 'http://rest.db.ripe.net/search?inverse-attribute=org&flags=no-referenced&source=ripe'

    LIRs = sum(args.orgs, [])
    for lir in LIRs:
        print(f'\n{lir}:')
        if args.v4:
            url = f"{base_url}&type-filter=inetnum&query-string={lir}"
            r = requests.get(url, headers=header)
            results = r.json()
            parse_inetnum_results(results, cidr, assigned, allocated, legacy, sub_allocated)
        if args.v6:
            url = f"{base_url}&type-filter=inet6num&query-string={lir}"
            r = requests.get(url, headers=header)
            results = r.json()
            parse_inet6num_results(results, assigned, allocated, legacy, sub_allocated)


if __name__ == '__main__':
    main()