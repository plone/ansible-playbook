Restart script
``````````````

One of the advantages of running a zeocluster configuration is that you may restart your Zope/Plone clients without downtime.
To make this easier, the Plone playbook builds a couple of utility scripts to coordinate restarts.
You'll find these scripts in the ``scripts`` subdirectory of your Plone install.

* ``restart_clients.sh`` restarts all clients sequentially.
* ``restart_single_client.sh`` will restart a single client.

Here's how it works.
The ``restart_clients.sh`` script will iterate through all of the clients for an install.
For each, it will:

* Mark the client "down" with the load balancer so that it's temporarily taken out of the cluster.
* Stop the client, wait a bit and restart it.
* Request one or more pages from this client for each virtual host operating on this Plone instance.
* Mark the client up with the load balancer so that it starts getting requests again.

Optionally, the script will finish by clearing the Varnish cache for each virtual host.
You may prevent this by adding ``noflush`` to the ``restart_clients.sh`` command line.

The ``restart_single_client.sh`` does the same for a single client, specified by number on the command line.
The Varnish cache is not touched.

Both scripts must be executed as superuser, usually via ``sudo``.
The extra permissions are required to control supervisor, haproxy and Varnish.

Restart script options
~~~~~~~~~~~~~~~~~~~~~~

The restart script mechanism setting ``warm_paths`` is used to specify paths that should be requested in order to warm the ZODB cache for the instance.
This is specified in a ``webserver_virtualhosts`` block.

warm_paths
~~~~~~~~~~

.. code-block:: yaml

    webserver_virtualhosts:
      - hostname: plone.org
        zodb_path: /Plone
        warm_paths:
            - /
            - /support
            - /contribute

In this example, the restart scripts will request the ZODB paths ``/Plone/``, ``/Plone/support`` and ``/Plone/contribute`` from each client before returning it to the load-balancer cluster.

The default value of ``warm_paths`` is ``/`` alone.


plone_restart_pre_script
~~~~~~~~~~~~~~~~~~~~~~~~

This may be specified globally or individually in ``webserver_virtualhosts``.

.. code-block:: yaml

    plone_restart_pre_script: |
        echo shell commands to run before restarting all clients

or:

.. code-block:: yaml

    playbook_plones:
      - plone_instance_name: primary
        plone_restart_pre_script: |
            echo shell commands to run before restarting all clients for this vhost


plone_restart_post_script
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

This may be specified globally or individually in ``webserver_virtualhosts``.

    plone_restart_post_script: |
        echo shell commands to run after restarting all clients

or:

.. code-block:: yaml

    playbook_plones:
      - plone_instance_name: primary
        plone_restart_post_script: |
            echo shell commands to run after restarting all clients for this vhost
