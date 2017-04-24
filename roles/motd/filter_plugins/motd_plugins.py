# Convenience functions to get logic out of playbooks/templates


def ports_from_plones(plones):
    """ Given playbook_plones, find all the ports in use in virtual hosts.
        Return sorted.
    """
    ports = []
    for plone in plones:
        for vhost in plone['webserver_virtualhosts']:
            port = vhost.get('port')
            if port is None:
                protocol = vhost.get('protocol', 'http')
                if protocol == 'https':
                    port = 443
                else:
                    port = 80
            else:
                port = int(port)
            ports.append(port)
    return sorted(set(ports))


def hostname_sorted_vhosts(vhosts):
    hosts = []
    for vhost in vhosts:
        if 'zodb_path' in vhost:
            hosts.append(vhost)
    return sorted(hosts, key=lambda a: a.get('hostname'))


class FilterModule(object):
    def filters(self):
        return {
            'ports_from_plones': ports_from_plones,
            'hostname_sorted_vhosts': hostname_sorted_vhosts,
        }
