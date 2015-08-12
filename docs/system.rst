Configuration options
---------------------


System options
``````````````

admin_email
~~~~~~~~~~~

.. code-block:: yaml

    admin_email: sysadmin@yourdomain.com

It is important that you update this setting. The admin_email address will receive system mail, some of which is vitally important.

If you don't set this variable, the playbook won't run.


motd
~~~~

.. code-block:: yaml

    motd: |
        Message of the day
        for your server

Sets the server's message of the day, which is displayed on login.

Defaults to:

.. code-block:: yaml

    motd: |
        This server is configured via Ansible.
        Do not change configuration settings directly.


auto_upgrades
~~~~~~~~~~~~~

.. code-block:: yaml

    auto_upgrades: (yes|no)

Should the operating system's auto-update feature be turned on. You will still need to monitor for updates that cannot be automatically applied and for cases where a system restart is required after an update.

Defaults to `yes`

.. warning ::

    Turning on automatic updates does not relieve you of the duty of actively administering the server. Many updates, including vital security updates, will not happen or take effect without direct action.


additional_packages
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    additional_packages:
        - sockstat

List any additional operating system packages you wish to install. Default is empty.

.. note ::

    The operating system packages necessary for the components in this kit are automatically handled when a part is installed.


timezone
~~~~~~~~

.. code-block:: yaml

    timezone: "America/Los_Angeles\n"

Specify the timezone that should be set on the server.  Default is "UTC\n".

.. note::

    The timezone string must be terminated with a newline character (\n).
