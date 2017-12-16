# -*- coding: utf-8 -*-
import argparse
import os
import sys

import definitions

from modules import dm, virt


def parse_options():
    """Handles the various options passed to the command line.
    It returns a argparse.Namespace.
    """

    parser = argparse.ArgumentParser(
                description='Provision a new Virtual Machine')
    subparsers = parser.add_subparsers(help='sub-command help')
    parser.add_argument('name', help='The name of the new virtual machine')
    parser.add_argument('--user', help='Username for the connection')
    parser.add_argument('--host', help='Hostname')
    # Create submenu 
    parser_create = subparsers.add_parser('create', help='Create a new VM')
    parser_create.add_argument('--vmtype', help='Type of VM',
                        choices=['pc-q35', 'pc-i440fx'],
                        required=True)
    parser_create_group_block = parser_create.add_argument_group('Disk devices options')
    parser_create_group_block.add_argument('--blocktype', help='Type of disks presented to the Guest',
						required=True, choices=['thinlv', 'file'])
    parser_create_group_block.add_argument('--filedevice', 
                        help='The image file used as storage')
    parser_create_group_block.add_argument('--lvpool', help='Thin pool LV to use to create the VM disk')
    parser_create_group_block.add_argument('--volumegroup', '-vg',
                        help='Thin pool Volume Group')
    parser_create_group_block.add_argument('--size', help='Size of the thin LV', default='10GB')
    parser_create_group_network = parser_create.add_argument_group('Network devices options')
    parser_create_group_network.add_argument('--networks', help='The number of networking devices')
    # Edit submenu
    parser_edit = subparsers.add_parser('edit', help='Edit VM')

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

    # We also restrict for now to only x86_64 machines
    usable_type = []
    for arch in types:
        if 'x86_64' in arch:
            for machine in types[arch]:
                usable_type.append(machine)

    match_type = False
    for t in usable_type:
        if args.vmtype in t:
            match_type = True

    if not match_type:
        print(("The hypervisor do not seem to support this type ({})"
               " of machine").format(args.vmtype))
        sys.exit(1)

    # Let's check the new VM name is not already used
    vms = virtual.list_vms_by_name(conn)
    if args.name in vms:
        print("The name {} is already used".format(args.name))
        conn.close()
        sys.exit(2)

    # Let's instantiate a device mapper object
    devm = dm.dmDev()
    # Create a thinlv
    errno, out, err = devm.create_thinlv(args.name, args.size,
                                         args.pool, args.volumegroup)
    if errno:
        print("An error occurred while creating the ThinLV:")
        print("\tStandard output: %" % out)
        print("\tStandard error: %" % out)

    # Create the vm based on the template
    newvm = virtual.create_vm(args.name,
                              conn,
                              os.path.join(definitions.TEMPLATE_PATH,
                              ("{}.{}".format(args.vmtype, "xml"))))

    print(newvm)

    conn.close()
    sys.exit(0)


if __name__ == "__main__":
    # execute only if run as a script
    main()

# vim: set et ts=4 sw=4 :
