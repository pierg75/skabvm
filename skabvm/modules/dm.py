import dmpy as dm


class dmDev(object):
    """Class to handle device mapper objects"""

    def __init__(self):
        self.lib_ver = dm.get_library_version()
        self.driver_ver = dm.driver_version()

    def list_devices(self):
        """List all device mapper devices"""
        dmt = dm.DmTask(dm.DM_DEVICE_LIST)
        dmt.run()
        for d in dmt.get_names():
            print("Device: %s (%d, %d)" % d)

    def list_targets(self):
        dmt = dm.DmTask(dm.DM_DEVICE_LIST_VERSIONS)
        dmt.run()
        versions = dmt.get_versions()
        for t in versions.keys():
            v = versions[t]
            print("%s (%d.%d.%d)" % (t, v[0], v[1], v[2]))
