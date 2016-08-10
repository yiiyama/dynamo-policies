"""
Classes defining site requirements.
"""

import common.configuration as config
import detox.configuration as detox_config

class NonzeroQuota(object):
    def __init__(self, group, included_sites = None):
        self.group = group
        self.included_sites = included_sites

    def __call__(self, site, partition, initial):
        if self.included_sites is not None and not self.included_sites.match(site.name):
            return False

        return site.group_quota(self.group) != 0


class GroupOccupancy(object):

    def __init__(self, group, included_sites = None):
        self.group = group
        self.included_sites = included_sites

    def __call__(self, site, partition, initial):
        """
        Argument partition is ignored
        """

        if self.included_sites is not None and not self.included_sites.match(site.name):
            return False

        if site.group_quota(self.group) == 0:
            return False

        if initial:
            return site.storage_occupancy(self.group) > detox_config.threshold_occupancy
        else:
            return site.storage_occupancy(self.group) > config.target_site_occupancy