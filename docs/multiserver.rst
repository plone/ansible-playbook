Multiple Plone Servers
``````````````````````

The easiest way to use this kit is when there is only one Plone installation for each server. It is possible, though, to support multiple Plones on a single server by customizing the playbook (or maintaining a separate playbook file if you wish to avoid repository merge problems).

Four of our roles are set up to handle multiple servers: the `plone_server` role, the `haproxy role`, the `varnish` role and the `nginx` role.

Here's a simple example in which we have two Plone servers, each with a ZEO configuration.


plone.plone_server
~~~~~~~~~~~~~~~~~~

We may set up multiple Plone backends by simply using the plone_server role multiple times, each time passing custom variables to the role:

.. code-block:: yaml

    - role: plone.plone_server
      plone_instance_name: primary_plone
      plone_target_path: /opt/primary_plone
      plone_var_path: /var/local/primary_plone
      plone_major_version: '5.0'
      plone_version: '5.0'
      plone_initial_password: admin
      plone_zeo_port: 5100
      plone_client_base_port: 5081
      plone_client_count: 2
      # plone_create_site: no

    - role: plone.plone_server
      plone_instance_name: secondary_plone
      plone_target_path: /opt/secondary_plone
      plone_var_path: /var/local/secondary_plone
      plone_major_version: '4.3'
      plone_version: '4.3.7'
      plone_initial_password: admin
      plone_zeo_port: 4100
      plone_client_base_port: 4081
      plone_client_count: 3
      # plone_create_site: no

haproxy
~~~~~~~

We can attach both clusters to load-balancer front ends with a single use of the `haproxy` role:

.. code-block:: yaml

    - role: haproxy
      tags: haproxy
      loadbalancer_clusters:
        - name: plone5_cluster
          port: 5080
          client_base_port: 5081
          client_count: 2
        - name: plone4_cluster
          port: 4080
          client_base_port: 4081
          client_count: 3

Likewise, a single use of the `varnish` role may specify multiple backends, disinguished by hostname:

.. code-block:: yaml

    - role: varnish
      tags: varnish
      proxycache_backends:
        - name: plone5
          port: 5080
          hostnames:
            - www.plone5site.org
            - www.plone5site.com
        - name: plone4
          port: 4080
          hostnames:
            - www.plone4site.org
            - www.plone4site.com

The Varnish setup makes use of the fact that the webserver passes hostnames in the virtual host URLs it creates.

nginx
~~~~~

The `nginx` role setup is no different than if we had a single Plone server, but we'll include it to complete the example:

.. code-block:: yaml

    - role: nginx
      when: install_webserver
      tags: nginx
      webserver_virtualhosts:
        - hostname: www.plone5site.org
          zodb_path: /Plone
          aliases:
            - www.plone5site.com
        - hostname: www.plone4site.org
          zodb_path: /Plone
          aliases:
            - www.plone4site.com
