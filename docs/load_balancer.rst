Load-balancer options
`````````````````````


install_loadbalancer
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_loadbalancer: (yes|no)

Do you want to use a load balancer? Defaults to ``yes``.

.. note ::

    If you decide not to use a load balancer, you will need to make sure that the ``loadbalancer_port`` setting points to your main ZEO client if you are using a proxy cache. If you are not using a proxy_cache, you must make sure that ``proxycache_port`` points to the main ZEO client.

Defaults to ``yes``.


loadbalancer_port
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    loadbalancer_port: 6080

The front-end port for the load balancer. Defaults to ``8080``.

.. note ::

    The haproxy stats page will be at ``http://localhost:1080/admin``. The administrative password is disabled on the assumption that the port will be firewalled and you will use an ssh tunnel to connect.


loadbalancer_options
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    loadbalancer_options: "maxconn 1 inter 10000 downinter 2000 rise 1 fall 2 on-error mark-down error-limit 15"

Use this variable to customize backend options for haproxy.
