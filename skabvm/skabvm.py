# -*- coding: utf-8 -*-
import argparse
import sys
import definitions

from modules import virt


def parse_options():
    """Handles the various options passed to the command line.
    It returns a argparse.Namespace.
    """

    parser = argparse.ArgumentParser(
                description='Provision a new Virtual Machine')
    parser.add_argument('name', help='The name of the new virtual machine')
    parser.add_argument('--user', help='Username for the connection')
    parser.add_argument('--host', help='Hostname')
    parser.add_argument('--blockdevice', '-b',
                        help='The block device used as storage')
    parser.add_argument('--filedevice', '-f',
                        help='The image file used as storage')
    parser.add_argument('--networks', '-n',
                        help='The number of networking devices')
    parser.add_argument('--vmtype', '-t',
                        help='Type of the VM',
                        choices=['pc-q35', 'pc-i440fx'])

    args = parser.parse_args()
    if args.user is None or args.host is None:
        print("You need to pass both the user and the host used to connect")
        print("to the hypervisor\n")
        parser.print_help()
        sys.exit(1)
    return args


def main():
    """The main function of skabvm"""
    args = parse_options()
    virtual = virt.libVirt(args.user, args.host)
    conn = virtual.connect()
    types = virtual.get_machine_type(virtual.caps(conn))
    # The pc-q35 is the latest machine type, so if possible let's use it
    # We also restrict for now to only x86_64 machines
    for arch in types:
        if 'x86_64' in arch:
            for machine in types[arch]:
                if 'pc-q35' in machine:
                    usable_type = machine

    # Let's check the new VM name is not already used
    vms = virtual.list_vms_by_name(conn)
    if args.name in vms:
        print("The name {} is already used".format(args.name))
        conn.close()
        sys.exit(2)

    print(vms)
    conn.close()
    sys.exit(0)


if __name__ == "__main__":
    # execute only if run as a script
    main()

# vim: set et ts=4 sw=4 :
