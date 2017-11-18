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
        return libvirt.open(auth_string)


# vim: set et ts=4 sw=4 :
