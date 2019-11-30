Monitoring options
``````````````````

install_muninnode
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_muninnode: (yes|no)

Do you want to install munin-node? Defaults to `yes`.

.. code-block:: yaml

    muninnode_query_ips:
        - 127.0.0.1
        - 192.168.10.3

What IP address are allowed to query your munin node? Specify a list of ip addresses.
Note that these will be converted to regular expressions by putting ``^`` and ``$`` at the beginning and end and escaping dots.

Defaults to ``127.0.0.1``

.. note::

    For this to be useful, you must set up a munin monitor machine and cause it to query your node.

munin_node_extra
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    munin_node_extra: "hostname_name test.example.com"

Adds code at the end of the munin-node configuration file.


install_logwatch
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_logwatch: (yes|no)

If turned on, this will cause a daily summary of log file information to be sent to the admin email address. Defaults to ``yes``.


install_fail2ban
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_fail2ban: (yes|no)

Fail2ban scans log files and bans IPs that show malicious signs -- too many password failures, seeking for exploits, etc. Defaults to ``yes``.

.. note::

    fail2ban is only useful with an iptables-style firewall.
