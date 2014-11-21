Web-server options
``````````````````

install_webserver
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_webserver: (yes|no)

Do you want to install Nginx? Defaults to ``yes``.

.. note ::

    If you decide not to install the webserver -- which acts as a reverse proxy -- you are on your own for making sure that Plone is accessible at a well-known port.

Virtual hosting setup
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    webserver_virtualhosts:
      - hostname: plone.org
        aliases:
          - www.plone.org
        zodb_path: /Plone
        port: 80
        protocol: http
        cnames:
            - www.plone.org
      - hostname: plone.org
        zodb_path: /Plone
        address: 92.168.1.150
        port: 443
        protocol: https
        certificate_file: /thiscomputer/path/mycert.crt
        key_file: /thiscomputer/path/mycert.key

Connects host names to paths in the ZODB. The ``address`` and ``port`` are used to construct the ``listen`` directive. If no address is specified, ``*`` will be used. If no port is specified, 80 will be used for http or 443 for https. If no protocol is specified, ``http`` will be used.

``cnames`` should be a list of hostname aliases that should be automatically redirected to the primary (or canonical). All the names on this list already should be in the aliases list.

Default value:

.. code-block:: yaml

    - hostname: localhost
      zodb_path: /Plone
      aliases:
        - default

.. note ::

    If you are setting up an https server, you must supply certificate and key files. The files will be copied from your local machine (the one containing the playbook) to the target server. Your key file must not be encrypted or you will not be able to start the web server automatically.

.. warning ::

    Make sure that your source key file is not placed in a public location.

