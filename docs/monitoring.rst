Monitoring options
``````````````````

install_muninnode
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_muninnode: (yes|no)

Do you want to install munin-node? Defaults to `yes`.

.. code-block:: yaml

    muninnode_query_ips:
        - ^127\.0\.0\.1$
        - ^192\.168\.10\.3$

What IP address are allowed to query your munin node? Specify a list of regular expressions.

Defaults to ``^127\.0\.0\.1$``

.. note ::

    For this to be useful, you must set up a munin monitor machine and cause it to query your node.


install_logwatch
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_logwatch: (yes|no)

If turned on, this will cause a daily summary of log file information to be sent to the admin email address. Defaults to `yes`


install_fail2ban
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_fail2ban: (yes|no)

Fail2ban scans log files and bans IPs that show malicious signs -- too many password failures, seeking for exploits, etc. Defaults to ``yes``.

.. note ::

    fail2ban is only useful with an iptables-style firewall.

