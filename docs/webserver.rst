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
        client_max_body_size: 4M
      - hostname: plone.org
        zodb_path: /Plone
        address: 92.168.1.150
        port: 443
        protocol: https
        certificate_file: /thiscomputer/path/mycert.crt
        key_file: /thiscomputer/path/mycert.key

Connects host names to paths in the ZODB. The ``address`` and ``port`` are used to construct the ``listen`` directive. If no address is specified, ``*`` will be used. If no port is specified, 80 will be used for http or 443 for https. If no protocol is specified, ``http`` will be used.

Default value:

.. code-block:: yaml

    webserver_virtualhosts:
      - hostname: localhost
        zodb_path: /Plone
        aliases:
          - default

.. note ::

    If you are setting up an https server, you must supply certificate and key files. The files will be copied from your local machine (the one containing the playbook) to the target server. Your key file must not be encrypted or you will not be able to start the web server automatically.

.. warning ::

    Make sure that your source key file is not placed in a public location.


Redirections, etc.
~~~~~~~~~~~~~~~~~~

If you do not specify a zodb_path, the webserver role will not automatically create a location stanza with a rewrite and proxy_pass directives.

If you specify ``extra``, the value will be copied into the server stanza.

Let's take a look at a common use for these options:

.. code-block:: yaml

    - hostname: plone.com
      protocol: http
      extra: return 301 https://$server_name$request_uri;

This is a *redirect to https* setting.


Status and monitoring
~~~~~~~~~~~~~~~~~~~~~

If you want to monitor your web server, make sure you have a "localhost" hostname or "default" alias with "http" protocol. This virtual server will have the status check set up on localhost.


You should know
~~~~~~~~~~~~~~~

When you do specify a zodb_path, so that the webserver role knows that you're working with Plone, it will block URLs containing "/manage\_" and will block http basic authentication. This means that it will be difficult to use the Zope Management Interface via the web server reverse proxy. Instead, use an SSH tunnel to the load balancer. Remember, this is a production installation. It *should* be hard to use the ZMI via the public interface.
