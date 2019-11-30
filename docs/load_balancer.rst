Load-balancer options
`````````````````````

install_loadbalancer
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_loadbalancer: (yes|no)

Do you want to use a load balancer? Defaults to ``yes``.

.. note::

    If you decide not to use a load balancer, you will need to make sure that the ``loadbalancer_port`` setting points to your main ZEO client if you are using a proxy cache. If you are not using a proxy_cache, you must make sure that ``proxycache_port`` points to the main ZEO client.

Defaults to ``yes``.


loadbalancer_port
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    loadbalancer_port: 6080

The front-end port for the load balancer. Defaults to ``8080``.

.. note::

    The haproxy stats page will be at ``http://localhost:1080/admin``. The administrative password is disabled on the assumption that the port will be firewalled and you will use an ssh tunnel to connect.


loadbalancer_healthcheck
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    loadbalancer_healthcheck: On

This option may be set to "On" or "Off" to turn haproxy health checks on or off for your ZEO clients.


loadbalancer_listen_extra
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    loadbalancer_listen_extra: "timeout connect 30s  # longer timeout for primary"

Use this variable to add configuration lines in ``listen`` sections.
Usually done to override defaults.
This variable may be set globally or in individual playbook_plones.


loadbalancer_options
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    loadbalancer_options: "maxconn 1 inter 10000 downinter 2000 rise 1 fall 2 on-error mark-down error-limit 15"

Use this variable to customize backend options for haproxy.
This is used with haproxy's ``default-server`` option.

.. note::

    Note the ``maxconn 1`` portion of the setting.
    This is meant to match up with the number of threads in use for each ZEO client.
    Be very cautious about setting ``maxconn`` higher than your ZEO thread count;
    it may result in requests being queued to a ZEO client even if it's busy and other ZEO clients are free.

    Also, if you're using health checks, you may want to read the haproxy docs and think seriously about how to avoid false positives that will mark a client down when it's handling a long request.
    Health check tests are made even when ``maxconn`` has been reached.
    You will want to make sure that ``inter`` anticipates the longest response time for the vast majority of your requests.
