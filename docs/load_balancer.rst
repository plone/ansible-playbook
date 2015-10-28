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


Multiple servers
````````````````

If you are setting up multiple Plone servers, you may specify multiple haproxy balanced clusters. Instead of the loadbalancer_* options listed above, specify the cluster as a list:

.. code-block:: yaml

    loadbalancer_clusters:
      - name: plone5_cluster
        port: 5080
        client_base_port: 5081
        client_count: 2
      - name: plone4_cluster
        port: 4080
        client_base_port: 4081
        client_count: 4
        options: "maxconn 2 inter 20000 downinter 4000 rise 1 fall 2 on-error mark-down error-limit 15"

Each item in the clusters list must have `name`, `port`, `client_base_port` and `client_count` specified. Setting `options` is optional. If options are not specified, the value of `loadbalancer_options` will be used.