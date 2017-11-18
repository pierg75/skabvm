# -*- coding: utf-8 -*-
import argparse
import sys
from modules import virt

def main():
    """The main function of skabvm"""
    args = parse_options()
    virt_conn = virt.libVirt(args.user, args.host)
    con = virt_conn.connect()
    types = virt_conn.get_machine_type(virt_conn.caps(con))
    # The pc-q35 is the latest machine type, so if possible let's use it
    # We also restrict for now to only x86_64 machines
    for arch in types:
        if 'x86_64' in arch:
            for machine in types[arch]:
                if 'pc-q35' in machine:
                    usable_type = machine

    print(usable_type)
    con.close()
    sys.exit(0)



def parse_options():
    """Handles the various options passed to the command line.
	It returns a argparse.Namespace.	
	"""

    parser = argparse.ArgumentParser(description='Provision a new Virtual Machine')
    parser.add_argument('name', help='The name of the new virtual machine')
    parser.add_argument('--user', help='Username for the connection')
    parser.add_argument('--host', help='Hostname')
    parser.add_argument('--blockdevice', '-b', help='The block device used as storage')
    parser.add_argument('--filedevice', '-f', help='The image file used as storage')
    parser.add_argument('--networks', '-n', help='The number of networking devices')

    args = parser.parse_args()
    if args.user is None or args.host is None:
        print("You need to pass both the user and the host used to connect")
        print("to the hypervisor\n")
        parser.print_help()
        sys.exit(1)
    return args

if __name__ == "__main__":
    # execute only if run as a script
    main()

# vim: set et ts=4 sw=4 :
