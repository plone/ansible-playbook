# Convenience functions for compiling and comparing lists of nginx virtual hosts

from os.path import basename


def expected_vhost_files(plones, inventory_hostname):
    """ Give a webserver_virtualhosts list, return a list of the
        filenames we expect to find in nginx/sites-enabled.
    """

    filenames = set()
    for aplone in plones:
        for vhost in aplone['webserver_virtualhosts']:
            hostname = vhost.get('hostname', inventory_hostname)
            protocol = vhost.get('protocol', 'http')
            filenames.add("{0}_{1}".format(protocol, hostname.replace('.', '_')))
    return filenames


def found_vhost_files(sites_found):
    """ sites_found should be from the Ansible find module.
        Parse it to return a set of filenames.
    """

    filenames = set()
    for afile in sites_found['files']:
        filenames.add(basename(afile['path']))
    return filenames


def unexpected_vhost_files(plones, inventory_hostname, sites_found):
    return found_vhost_files(sites_found) - expected_vhost_files(plones, inventory_hostname)


def expected_supervisor_files(plones, supervisor_ext):
    """ from a list of plones, learn our expected supervisor/conf.d files.
    """

    filenames = set()
    for aplone in plones:
        filenames.add("{0}_zeo{1}" .format(aplone.get('plone_instance_name', 'zeoserver'), supervisor_ext))
    return filenames


def unexpected_supervisor_files(plones, sites_found, supervisor_ext):
    return found_vhost_files(sites_found) - expected_supervisor_files(plones, supervisor_ext)


class FilterModule(object):
    def filters(self):
        return {
            'expected_vhost_files': expected_vhost_files,
            'found_files': found_vhost_files,
            'unexpected_vhost_files': unexpected_vhost_files,
            'expected_supervisor_files': expected_supervisor_files,
            'unexpected_supervisor_files': unexpected_supervisor_files,
        }
