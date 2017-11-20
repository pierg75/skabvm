import sys

import dmpy as dm


class dmDev(object):
    """Class to handle device mapper objects"""

    def __init__(self):
        self.lib_ver = dm.get_library_version()
        self.driver_ver = dm.driver_version()
        self.targets = self.list_targets()
        try:
            self.targets['thin-pool'] or self.targets['thin']
        except KeyError:
            print("The thin pool module is not loaded")
            sys.exit(2)

    def list_devices(self):
        """List all device mapper devices"""
        dmt = dm.DmTask(dm.DM_DEVICE_LIST)
        dmt.run()
        for d in dmt.get_names():
            print("Device: %s (%d, %d)" % d)

    def list_targets(self):
        dmt = dm.DmTask(dm.DM_DEVICE_LIST_VERSIONS)
        dmt.run()
        return dmt.get_versions()

    def create_thinlv(self, name, size, pool):
        """This should basically do what the function _create() in 
        tools/dmsetup.c does. I guess we can probably better do a 
        generic create() and then a special case for thinlv.
        Note: This doesn't yet work

        """
        dmt_thin = dm.DmTask(dm.DM_DEVICE_CREATE)
        dmt_thin.set_name(name)
        dmt_thin.
        dmt_thin.set_message('0 390625 thin /dev/mapper/testvg-pool0 20')
        dmt_thin.run()
