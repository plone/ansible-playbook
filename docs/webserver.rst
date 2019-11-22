Web-server options
``````````````````

install_webserver
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_webserver: (yes|no)

Do you want to install Nginx? Defaults to ``yes``.

.. note::

    If you decide not to install the webserver—which acts as a reverse proxy—you are on your own for making sure that Plone is accessible at a well-known port.

Virtual hosting setup
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    webserver_virtualhosts:
      - hostname: plone.org
        default_server: yes
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

Connects host names to paths in the ZODB. The ``address`` and ``port`` are used to construct the ``listen`` directive. If no address is specified, ``*`` will be used. If no port is specified, ``80`` will be used for http or ``443`` for https. If no protocol is specified, ``http`` will be used.

Default value:

.. code-block:: yaml

    webserver_virtualhosts:
      - hostname: "{{ inventory_hostname }}"
        default_server: yes
        zodb_path: /Plone
        aliases:
          - default
        client_max_body_size: 2M

.. note::

    If you are setting up an https server, you must supply certificate and key files in one of two ways. Details are in the following Certificates section.

    You may set ``client_max_body_size`` globally.
    If you set it in virtual host blocks, it overrides the global setting.

Certificates
~~~~~~~~~~~~

If you are setting up an https server, you must supply certificate and key files.

.. warning::

    Your key file must not be encrypted or you will not be able to start the web server automatically.

Certificate files may be specified in one of two ways.

To copy certificate files from the machine running Ansible, use the format:

.. code-block:: yaml

    webserver_virtualhosts:
      - hostname: ...
        ...
        certificate_file: /thiscomputer/path/mycert.crt
        key_file: /thiscomputer/path/mycert.key

To use files that already exist on the controlled server, use:

.. code-block:: yaml

    webserver_virtualhosts:
      - hostname: ...
        ...
        certificate:
          key: /etc/ssl/private/ssl-cert-snakeoil.key
          crt: /etc/ssl/certs/ssl-cert-snakeoil.pem


Redirections, etc.
~~~~~~~~~~~~~~~~~~

If you do not specify a ``zodb_path``, the webserver role will not automatically create a location stanza with a rewrite and ``proxy_pass`` directives.

If you specify ``extra``, the value will be copied into the server stanza before the ``location`` setions.

Let's take a look at a common use for these options:

.. code-block:: yaml

    - hostname: plone.com
      protocol: http
      extra: return 301 https://$server_name$request_uri;

This is a *redirect to https* setting.

``location_extra`` may be used to add directives *within* the location block:

.. code-block:: yaml

    - hostname: plone.com
      protocol: http
      location_extra: |
        auth_basic "Private Demo - please enter your credentials";
        auth_basic_user_file /etc/nginx/htpasswd;


Inside-out hosting
~~~~~~~~~~~~~~~~~~

Zope "inside-out" virtual hosting allows you to direct URLs for a subpath to a ZODB location.
The subpath is stripped by the Zope Virtual Host Monster.

.. code-block:: yaml

    - hostname: plone.com
      zodb_path: plone_vendors
      location_subfolder: vendors

URLs starting with ``plone.com/vendors`` will be served from the ZODB path ``/plone_vendors``.
Other plone.com URLs will be unaffected.


rewrite_server_name
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    - hostname: plone.com
      aliases:
        www.plone.com
      default_server: yes
      rewrite_server_name: host
      ...

When we use nginx to rewrite URLs for Zope/Plone, we normally use the nginx variable ``$server_name`` to stand in for the hostname.
The nginx ``$server_name`` variable picks up the primary hostname -- the one specified by the hostname variable of the ``webserver_virtualhosts`` list item.
You may or may not want this behavior, as the resources that Plone links to will be referenced at that canonical hostname.

If, instead, you wish the rewrites to use whatever hostname is specified, then you'll want to use the nginx ``$host`` variable instead.
Make sure you test, as the ``$host`` variable can be a bit flaky in real use.


Status and monitoring
~~~~~~~~~~~~~~~~~~~~~

If you want to monitor your web server, make sure you have a ``localhost`` hostname or ``default`` alias with ``http`` protocol. This virtual server will have the status check set up on localhost.


You should know
~~~~~~~~~~~~~~~

When you do specify a ``zodb_path``, so that the webserver role knows that you're working with Plone, it will block URLs containing ``/manage\_`` and will block http basic authentication. This means that it will be difficult to use the Zope Management Interface via the web server reverse proxy. Instead, use an SSH tunnel to the load balancer. Remember, this is a production installation. It *should* be hard to use the ZMI via the public interface.

SSL Settings
~~~~~~~~~~~~

**SSL Protocols**

Globally:

.. code-block:: yaml

    ssl_protocols: "{{ intermediate_protocols }}"

or, per-server:

.. code-block:: yaml

    - hostname: plone.com
      protocol: https
      ssl_protocols:  "{{ intermediate_protocols }}"

Use this variable to control SSL protocols either globally or per virtual server.
You may set these as a simple string or make use of one of three variables:

- ``modern_protocols``
- ``intermediate_protocols``
- ``old_protocols``

"Modern", "Intermediate", and "Old" are meant to match the matching settings from Mozilla's `Security/Server Side TLS <https://wiki.mozilla.org/Security/Server_Side_TLS>`_ recommendations.

Default value:

.. code-block:: yaml

    ssl_protocols: "{{ modern_protocols }}"


**SSL Ciphers**

Globally:

.. code-block:: yaml

    ssl_ciphers: "{{ intermediate_ciphers }}"

or, per-server:

.. code-block:: yaml

    - hostname: plone.com
      protocol: https
      ssl_ciphers:  "{{ intermediate_ciphers }}"

Use this variable to control SSL ciphers either globally or per virtual server.
You may set these as a simple string or make use of one of three variables:

- ``modern_ciphers``
- ``intermediate_ciphers``
- ``old_ciphers``

"Modern", "Intermediate", and "Old" are meant to match the matching settings from Mozilla's `Security/Server Side TLS <https://wiki.mozilla.org/Security/Server_Side_TLS>`_ recommendations.

Default value:

.. code-block:: yaml

    ssl_ciphers: "{{ modern_ciphers }}"

**Shared SSL Settings**

.. code-block:: yaml

    ssl_shared_conf: |
      ssl_session_timeout 1h;
      ssl_session_cache shared:SSL:5m;
      ssl_session_tickets off;

The value of this variable is written into the nginx ``conf.d`` directory as the file ``ssl_shared.conf``.
Use this to change SSL settings that are meant to apply globally or may only be set once.

Default value:

.. code-block:: yaml

    ssl_shared_conf: |
      ssl_session_timeout 1d;
      ssl_session_cache shared:SSL:50m;
      {% if nginx_v_result.stdout is version('1.5.9', 'ge') %}ssl_session_tickets off;{% endif %}

The last line assures that the ssl_session_tickets parameter is only set on versions of nginx that allow it.


**http2**

.. code-block:: yaml

    allow_http2: no

If your nginx version is >= 1.9.5, we turn on http2 for https virtual hosts.
You may globally block this behavior by setting ``allow_http2`` to ``no``.

.. code-block:: yaml

    allow_http2: yes
