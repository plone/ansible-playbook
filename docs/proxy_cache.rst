Caching proxy options
`````````````````````


install_proxycache
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_proxycache: (yes|no)

Do you want to install the Varnish reverse-proxy cache? Default is ``yes``.

.. note ::

    If you decide not to use a proxy cache, you will need to make sure that the ``proxycache_port`` setting points to your load balancer front end. If you are not using a load balancer, you must make sure that ``proxycache_port`` points to main ZEO client.


proxycache_port
~~~~~~~~~~~~~~~

.. code-block:: yaml

    proxycache_port: 5081

The front-end address for the proxy cache. Defaults to ``6081``.

.. note ::

    We assume the varnish cache and admin ports are firewalled and that you will administer the cache via ssh.


proxycache_size
~~~~~~~~~~~~~~~

.. code-block:: yaml

    proxycache_size: 512m

Sets the Varnish cache size. Default is ``256m`` -- 256 megabytes.

