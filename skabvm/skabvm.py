# -*- coding: utf-8 -*-
import argparse


def main():
    """The main function of skabvm"""
    args = parse_options()
    print("{}".format(args))


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

    return parser.parse_args()
    


class libVirt(object):
    """A connection to the hypervisor.

    Attributes:
        user: The username for the connection
        host: The hostname for the connection
        
    """

    def __init__(self, user, host):
        """Returns a libVirt object where conn is *connection*"""
        self.user = user
        self.host = host

    def connect(self):
        """Connects to the hypervisor using *connection* passed at initialization.
        It may require to provide a password (for now we use by default root)
        """
        auth_string = ("qemu+ssh://{}@{}/system".format(self.user, self.host))
        return libvirt.open(auth_string)



if __name__ == "__main__":
    # execute only if run as a script
    main()

# vim: set et ts=4 sw=4 :
