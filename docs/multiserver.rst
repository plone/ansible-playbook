Multiple Plone Servers
``````````````````````

The easiest way to use this kit is when there is only one Plone installation for each server. You may, though, use it to install multiple Plone instances to a single server. Up to four Plone instances are supported per server. More may be added via minor customization of the playbook.

To install multiple Plone instances to a server, specify all settings that are unique per instance in a ``playbook_plones`` list. Settings that are not specific to a particular server may be set as usual.

At a minimum, you must set specific values for ``plone_instance_name`` and for the Plone and load-balancer ports. You'll usually also want to set virtual host settings.

Here's a minimal example:

.. code-block:: yaml

    playbook_plones:
      - plone_instance_name: primary
        plone_zeo_port: 8100
        plone_client_base_port: 8081
        loadbalancer_port: 8080
        webserver_virtualhosts:
          - hostname: "{{ inventory_hostname }}"
            aliases:
              - default
            zodb_path: /Plone
      - plone_instance_name: secondary
        plone_zeo_port: 7100
        plone_client_base_port: 7081
        loadbalancer_port: 7080
        webserver_virtualhosts:
          - hostname: www.plone.org
            zodb_path: /Plone

Dispatching requests to the matching Plone instance occurs in Varnish, and is done by hostname. So, in the example above, when Varnish sees ``www.plone.org`` in a request URL, it will send the request to port 7080, our secondary instance.

Remember, all the settings except the ones in ``playbook_plones`` are set as documented elsewhere.

Nearly all the ``plone_*`` variables, and a few others like ``loadbalancer_port`` and ``webserver_virtualhosts`` may be set in ``playbook_plones``. Let's take a look at a more sophisticated instance list that handles two different versions of Plone:

.. code-block:: yaml

    playbook_plones:
      plone_instance_name: primary_plone
      plone_target_path: /opt/primary_plone
      plone_var_path: /var/local/primary_plone
      plone_major_version: '5.0'
      plone_version: '5.0'
      plone_initial_password: admin
      plone_zeo_port: 5100
      loadbalancer_port: 4080
      plone_client_base_port: 5081
      plone_client_count: 2
      plone_create_site: no
      webserver_virtualhosts:
        - hostname: plone.org
          zodb_path: /plone_org
          aliases:
            - www.plone.org
    - plone_instance_name: secondary_plone
      plone_target_path: /opt/secondary_plone
      plone_var_path: /var/local/secondary_plone
      plone_major_version: '4.3'
      plone_version: '4.3.7'
      plone_initial_password: admin
      plone_zeo_port: 4100
      loadbalancer_port: 4080
      plone_client_base_port: 4081
      plone_client_count: 3
      plone_create_site: no
      webserver_virtualhosts:
        - hostname: plone.com
          zodb_path: /plone_com
          aliases:
            - www.plone.com
        - hostname: plone.com
          zodb_path: /plone_com
          address: 92.168.1.150
          port: 443
          protocol: https
          certificate_file: /thiscomputer/path/mycert.crt
          key_file: /thiscomputer/path/mycert.key

Moving beyond four
------------------

Ansible doesn't offer a way to iterate a role over a sequence, so the max count of four is hard-coded into the playbook. Read the playbook and it will be obvious how to change the limit by editing it.