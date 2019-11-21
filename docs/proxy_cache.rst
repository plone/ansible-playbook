Caching proxy options
`````````````````````


install_proxycache
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_proxycache: (yes|no)

Do you want to install the Varnish reverse-proxy cache? Default is ``yes``.

.. note::

    If you decide not to use a proxy cache, you will need to make sure that the ``proxycache_port`` setting points to your load balancer front end. If you are not using a load balancer, you must make sure that ``proxycache_port`` points to the main ZEO client.


proxycache_port
~~~~~~~~~~~~~~~

.. code-block:: yaml

    proxycache_port: 5081

The front-end address for the proxy cache. Defaults to ``6081``.

.. note::

    We assume the varnish cache and admin ports are firewalled and that you will administer the cache via ``ssh``.


proxycache_size
~~~~~~~~~~~~~~~

.. code-block:: yaml

    proxycache_size: 512m

Sets the Varnish cache size. Default is ``256m`` -- 256 megabytes.


proxycache_method
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    proxycache_method: file

Use this to specify Varnish's cache mechanism. Default is ``malloc``.


proxy_cache_block_basic_auth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml
    proxy_cache_block_basic_auth: off

Use this variable to determine whether or not Varnish blocks the HTTP Authorization header, which is used in basic auth.
This is set to ``on`` by default, thus blocking Zope's basic auth, which generally should not be exposed to the Internet.


Cache controls
~~~~~~~~~~~~~~

These settings fine-tune the cache rules.

.. code-block:: yaml

    # allow compression for all except these extensions
    nocompress_ext: (jpg|png|gif|gz|tgz|bz2|tbz|mp3|ogg)

    # never set cookies on responses with these extensions
    no_response_cookie_ext: (pdf|asc|dat|txt|doc|xls|ppt|tgz|png|gif|jpeg|jpg|ico|swf|css|js)

    # To improve caching, on incoming requests remove all except these cookies
    cache_sanitize_cookie_exceptions: (statusmessages|__ac|_ZopeId|__cp)

    # When these cookies are not found, mark request with
    # X-Anonymous header to allow split caching.
    nonanonymous_cookies: __ac(|_(name|password|persistent))

    # Adds miscellaneous VCL in vcl_recv; see the template files for location
    proxy_cache_vcl_extra:

    # Adds code inside backend stanzas. Most commonly used to set timeouts.
    proxy_cache_backend_extra:

Defaults are as indicated in the example. Don't change these without giving it some thought.
