Configuration options
---------------------

Ansible options
```````````````

ansible_ssh_pipelining
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    ansible_ssh_pipelining: true

The Plone server role uses ssh pipelining to avoid security errors from Ansible when running operations without superuser rights.
SSH pipelining for this purpose may require the disabling of ``requiretty`` in ``/etc/sudoers``.
If you get a pipelining error and cannot disable ``requiretty``, set this variable to ``false`` and instead turn on ``allow_world_readable_tmpfiles`` in your ``ansible.cfg``.
See http://docs.ansible.com/ansible/become.html#becoming-an-unprivileged-user for a discussion.


System options
``````````````

admin_email
~~~~~~~~~~~

.. code-block:: yaml

    admin_email: sysadmin@yourdomain.com

It is important that you update this setting. The ``admin_email`` address will receive system mail, some of which is vitally important.

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

Defaults to ``yes``.

.. warning::

    Turning on automatic updates does not relieve you of the duty of actively administering the server. Many updates, including vital security updates, will not happen or take effect without direct action.


additional_packages
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    additional_packages:
        - sockstat

List any additional operating system packages you wish to install. Default is empty.

.. note::

    The operating system packages necessary for the components in this kit are automatically handled when a part is installed.


timezone
~~~~~~~~

.. code-block:: yaml

    timezone: "America/Los_Angeles"

Specify the timezone that should be set on the server.  Default is ``UTC``.

.. note::

    The timezone string must be terminated with a newline character (``\n``).

set_timezone
~~~~~~~~~~~~

.. code-block:: yml

    set_timezone: no

If you have a reason to prevent setting the timezone, set this to ``no``.
Default is ``yes``.


logwatch_ignore
~~~~~~~~~~~~~~~

.. code-block:: yml

    logwatch_ignore: |
      Received disconnect from
      Disconnected from
      message repeated \d+ times: \[ Failed password for root from
      maximum authentication attempts exceeded for root

Sets the contents of the logwatch ``ignore.conf`` file.
Each line should be a regular expression.
If matched, the log line will be ignored and unconsidered in any log-based report.
Use with great caution to reduce noice in your logwatch report.
