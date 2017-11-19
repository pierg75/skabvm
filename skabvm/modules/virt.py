import sys
from xml.etree import ElementTree

import libvirt


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
        try:
            conn = libvirt.open(auth_string)
        except libvirt.libvirtError:
            sys.exit(1)
        return conn

    def caps(self, conn):
        """It gets the capabilities of the hypervisor

        Attributes:
            conn:   The virConnect class returned from a libvirt.open*() call

        """
        try:
            caps = conn.getCapabilities()
        except:
            print("Unexpected error while retrieving hypervisor capabilities")
            sys.exit(1)
        return caps

    def get_machine_type(self, caps):
        """It analyses a XML output from getCapabilities().
        It returns a dictionary where the keys are the architectures
        supported and the values a list of possible machine types.

        Attributes:
            caps = string representing the capabilities XML

        """

        d = {}
        machines = []
        tree = ElementTree.fromstring(caps)
        for guest in tree.findall('guest'):
            for arch in guest.findall('arch'):
                for m in arch.findall('machine'):
                    machine = m.get('canonical')
                    if machine is not None:
                        machines.append(machine)
                d[arch.get('name')] = machines
                machines = []
        return d

    def list_vms_by_name(self, conn):
        """It lists all the VMs on this hypervisor.

        Attributes:
            conn: The virConnect class returned from a libvirt.open*() call
        """
        try:
            vms = conn.listDefinedDomains()
        except:
            print("Unexpected error while retrieving list of VMs")
            sys.exit(1)
        return vms

    def create_vm(self, conn, template):
        """It creates a new VM based on a template.

        Attributes:
            conn: The virConnect class returned from a libvirt.open*() call
            template: The path to the type of the template
        """
        xml = ""
        with open(template, "r") as file:
            xml = file.read()
        try:
            vm = conn.defineXML(xml)
        except:
            print("Unexpected error while creating list of VMs")
            sys.exit(1)
        return vm

# vim: set et ts=4 sw=4 :
