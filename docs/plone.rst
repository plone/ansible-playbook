Plone options
`````````````

plone_initial_password
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_initial_password: alnv%r(ybs83nt

Initial password of the Zope ``admin`` user. The initial password is used when the database is first created.

Defaults to ``""`` -- which will fail.


plone_target_path
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_target_path: /opt/plone

Sets the Plone installation directory.

Defaults to ``/usr/local/plone-{{ plone_major_version }}``


plone_var_path
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_var_path: /var/plone_var

Sets the Plone installation directory.

Defaults to ``/var/local/plone-{{ plone_major_version }}``


plone_buildout_git_repo
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    buildout_git_repo: https://github.com/plone/plone.com.ansible.git
    buildout_git_version: master

``buildout_git_repo`` defaults to none (uses built-in buildout).

``buildout_git_version`` is the tag or branch. Defaults to ``master``.

.. note::

    If you use your own buildout from a repository, you still need to specify your client count so that the playbook can 1) set up the supervisor specifications to start/stop and monitor clients, and 2) set up the load balancer.

    Client part names must follow the pattern `client#` where # is a number (1,2,3 ...). Client ports must be numbered sequentially beginning with 8081 or the value you set for plone_client_base_port. The zeoserver part must be named `zeoserver` and be at 8100 or the value you set for plone_zeo_port.

    If you use your own buildout, all Plone settings except ``plone_client_count``, ``plone_client_base_port``, and ``plone_client_max_memory`` are ignored.

plone_major_version
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_version: '5.0'

plone_version
~~~~~~~~~~~~~

.. code-block:: yaml

    plone_version: '5.0'

Which Plone version do you wish to install? This defaults to the current stable version at the time you copy or clone the playbook. Both plone_major_version and plone_version should be quoted so that they will be interpreted as strings.

plone_client_count
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_client_count: 5

How many ZEO clients do you want to run?

Defaults to ``2``

.. note ::

    The provided buildout always creates an extra client ``client_reserve`` that is not hooked into supervisor or the load balancer.
    Use it for debugging, running scripts and quick testing.
    If you need to remotely connect to the reserve client, you'll typically do that via an ssh tunnel.


plone_zodb_cache_size
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_zodb_cache_size: 30000

How many objects do you wish to keep in the ZODB cache.

Defaults to ``30000``

.. Note ::

    The default configuration is *very* conservative to allow Plone to run in a minimal memory server. You will want to increase this if you have more than minimal memory.


plone_zserver_threads
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_zserver_threads: 2

How many threads should run per server?

Defaults to ``1``


plone_client_max_memory
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_client_max_memory: 800MB

A size (suffix-multiplied using “KB”, “MB” or “GB”) that should be considered “too much”. If any Zope/Plone process exceeds this maximum, it will be restarted. Set to ``0`` for no memory monitoring.

Defaults to ``0`` (turned off)

.. note ::

    This setting is used in configuration of the ``memmon`` monitor in supervisor: `superlance <http://superlance.readthedocs.org/en/latest>`_ plugin.


plone_additional_eggs
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_additional_eggs:
        - Products.PloneFormGen
        - collective.cover
        - webcouturier.dropdownmenu

List additional Python packages (beyond Plone and the Python Imaging Library) that you want available in the Python package environment.

The default list is empty.

.. note ::

    Plone hotfixes are typically added as additional eggs.


plone_sources
~~~~~~~~~~~~~

.. code-block:: yaml

    plone_sources:
      -  "my.package = svn http://example.com/svn/my.package/trunk update=true"
      -  "some.other.package = git git://example.com/git/some.other.package.git rev=1.1.5"

This setting allows you to check out and include repository-based sources in your buildout.

Source specifications, a list of strings in `mr.developer <https://pypi.python.org/pypi/mr.developer>`_ sources format. If you specify plone_sources, the mr.developer extension will be used with auto-checkout set to "*" and git_clone_depth set to "1".

Private repository source present a special challenge. The typical solution will be to set up a repository user with the ssh public key for the plone_buildout user.


plone_zcml_slugs
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_zcml_slugs:
        - plone.reload

List additional ZCML slugs that may be required by older packages that don't implement auto-discovery. The default list is empty. This is rarely needed.


plone_additional_versions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_additional_versions:
      - "Products.PloneFormGen = 1.7.16"
      - "Products.PythonField = 1.1.3"
      - "Products.TALESField = 1.1.3"

The version pins you specify here will be added to the ``[versions]`` section of your buildout. The default list is empty.


plone_zeo_port
~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_zeo_port: 6100

The port number for the Zope database server. Defaults to ``8100``.


plone_client_base_port
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_client_base_port: 6080

The port number for your first Zope client. Subsequent client ports will be added in increments of 1. Defaults to ``8081``.

plone_environment_vars
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_environment_vars:
        - "TZ US/Eastern"
        - "zope_i18n_allowed_languages en"

A list of environment variables you wish to set for running Plone instances.

Defaults to:

.. code-block:: yaml

    - "PYTHON_EGG_CACHE ${buildout:directory}/var/.python-eggs"


plone_client_extras
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_client_extras: |
        z2-log-level = error

Extra text to add to all the client buildout parts. Defaults to "".


plone_client1_extras
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_client1_extras: |
        webdav-address = 9080
        ftp-address = 8021

Extra text to add to only the first client buildout part. Defaults to "".


plone_autorun_buildout
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_autorun_buildout: (yes|no)

Do you wish to automatically run buildout if any of the Plone settings change? Defaults to ``yes``.


plone_buildout_cache_url
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_buildout_cache_url: http://dist.plone.org/4.3.4/buildout-cache.tar.bz2

The URL of a buildout egg cache. Defaults to the one for the current stable version of Plone.


plone_buildout_cache_file
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_buildout_cache_file: /home/steve/buildout-cache.tar.bz2

The full local (host) filepath of a buildout egg cache. Defaults to none. Should not be used at the same time as plone_buildout_cache_url.


supervisor_instance_discriminator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    supervisor_instance_discriminator: customer_15

Optionally use this variable when you're installing multiple plone servers on the same machine.
The value for supervisor_instance_discriminator will be set as a prefix to all supervisor jobs for this plone server.

You do not need to set a supervisor_instance_discriminator if the servers have different instance names.


Cron jobs
~~~~~~~~~

plone_pack_at
~~~~~~~~~~~~~

.. code-block:: yaml

    plone_pack_at:
      minute: 30
      hour: 1
      weekday: 7

When do you wish to run the ZEO pack operation? Specify minute, hour and weekday specifications for a valid *cron* time. See ``CRONTAB(5)``. Defaults to 1:30 Sunday morning. Set to ``no`` to avoid creation of a cron job.


plone_keep_days
~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_keep_days: 3

How many days of undo information do you wish to keep when you pack the database. Defaults to ``3``.


plone_backup_at
~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_backup_at:
      minute: 30
      hour: 2
      weekday: "*"

When do you wish to run the backup operation?  Specify minute, hour and weekday specifications for a valid *cron* time. See ``CRONTAB(5)``. Defaults to 2:30 every morning.  Set to ``no`` to avoid creation of a cron job.


plone_keep_backups
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_keep_backups: 3

How many generations of full backups do you wish to keep? Defaults to ``2``.

.. note ::

    Daily backups are typically partial: they cover the differences between the current state and the state at the last full backup. However, backups after a pack operation are complete (full) backups -- not incremental ones. Thus, keeping two full backups means that you have backups for ``plone_keep_backups * days_between_packs`` days. See the `collective.recipe.backup documentation <https://pypi.python.org/pypi/collective.recipe.backup>`_.


plone_keep_blob_days
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_keep_blob_days: 21

How many days of blob backups do you wish to keep? This is typically set to `keep_backups * days_between_packs`` days. Default is ``14``.

plone_backup_path
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_backup_path: /mnt/backup/plone

Where do you want to put your backups? The destination must be writable by the ``plone_daemon`` user. Defaults to ``./var`` inside your buildout directory. Subdirectories are created for blob and filestorage backups.
