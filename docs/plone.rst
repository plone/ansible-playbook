Plone options
`````````````

plone_initial_password
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_initial_password: alnv%r(ybs83nt

Initial password of the Zope ``admin`` user. The initial password is used when the database is first created.

Defaults to ``""`` -- which will fail.


plone_buildout_cfg
~~~~~~~~~~~~~~~~~~

    plone_buildout_cfg: buildout.cfg

Sets the filename of the main buildout file. Default to ``live.cfg``.


plone_target_path
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_target_path: /opt/plone

Sets the Plone installation directory.

Defaults to ``/usr/local/plone-{{ plone_major_version }}``.


plone_var_path
~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_var_path: /var/plone_var

Sets the Plone installation directory.

Defaults to ``/var/local/plone-{{ plone_major_version }}``.


plone_buildout_git_repo
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_buildout_git_repo: https://github.com/plone/plone.com.ansible.git
    plone_buildout_git_version: master

``plone_buildout_git_repo`` defaults to none (uses built-in buildout).

``plone_buildout_git_version`` is the tag or branch. Defaults to ``master``.

.. note::

    If you use your own buildout from a repository, you still need to specify your client count so that the playbook can 1) set up the supervisor specifications to start/stop and monitor clients, and 2) set up the load balancer.

    Client part names must follow the pattern ``client#`` where # is a number (1, 2, 3, ...). Client ports must be numbered sequentially beginning with ``8081`` or the value you set for ``plone_client_base_port``. The zeoserver part must be named ``zeoserver`` and be at ``8100`` or the value you set for ``plone_zeo_port``.

    If you use your own buildout, all Plone settings except ``plone_client_count``, ``plone_client_base_port``, and ``plone_client_max_memory`` are ignored.


plone_major_version
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_version: '5.0'


plone_version
~~~~~~~~~~~~~

.. code-block:: yaml

    plone_version: '5.0'

Which Plone version do you wish to install? This defaults to the current stable version at the time you copy or clone the playbook. Both ``plone_major_version`` and ``plone_version`` should be quoted so that they will be interpreted as strings.


plone_python_version
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_python_version: '2.7'

For Plone 5.2+, you may specify ``'2.7'`` or ``'3'``.
Earlier Plones must use ``'2.7'``.
Defaults to ``'2.7'``.


plone_client_count
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_client_count: 5

How many ZEO clients do you want to run?

Defaults to ``2``.

.. note::

    The provided buildout always creates an extra client ``client_reserve`` that is not hooked into supervisor or the load balancer.
    Use it for debugging, running scripts and quick testing.
    If you need to remotely connect to the reserve client, you'll typically do that via an ssh tunnel.


plone_zodb_cache_size
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_zodb_cache_size: 30000

How many objects do you wish to keep in the ZODB cache.

Defaults to ``30000``.

.. note::

    The default configuration is *very* conservative to allow Plone to run in a minimal memory server. You will want to increase this if you have more than minimal memory.


plone_zserver_threads
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_zserver_threads: 2

How many threads should run per server?

Defaults to ``1``.


plone_client_max_memory
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_client_max_memory: 800MB

A size (suffix-multiplied using ``KB``, ``MB``, or ``GB``) that should be considered "too much". If any Zope/Plone process exceeds this maximum, it will be restarted. Set to ``0`` for no memory monitoring.

plone_hot_monitor
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_hot_monitor: cron

The *hot monitor* is the mechanism used to check for and act on processes exceeding the ``plone_client_max_memory`` setting.
There are two available mechanisms:

* `superlance <http://superlance.readthedocs.org/en/latest>`_ is a supervisor plugin.
  Its memory-monitor mechanisms are well-known in the Plone community and well-tested.
  If a Zope/Plone process exceeds the max memory setting, the equivalent of a supervisor process restart occurs.

* ``cron`` is a mechanism installed by the Plone Ansible Playbook.
  It uses a cron job to check twice an hour for clients that pass the threshold.
  If an offending client is found, the ``scripts/restart_single_client.sh`` script is used to restart the client.
  This script removes the client from the haproxy cluster before restarting, then loads pages to warm the ZODB cache before returning the client to the load-balancer cluster.
  The ``cron`` option was added in version 1.2.17 of the Playbook. It's implemented in the ``restart_script`` role.

Defaults to ``superlance``.

plone_additional_eggs
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_additional_eggs:
        - Products.PloneFormGen
        - collective.cover
        - webcouturier.dropdownmenu

List additional Python packages (beyond Plone and the Python Imaging Library) that you want available in the Python package environment.

The default list is empty.

.. note::

    Plone hotfixes are typically added as additional eggs.


plone_sources
~~~~~~~~~~~~~

.. code-block:: yaml

    plone_sources:
      -  "my.package = svn http://example.com/svn/my.package/trunk update=true"
      -  "some.other.package = git git://example.com/git/some.other.package.git rev=1.1.5"

This setting allows you to check out and include repository-based sources in your buildout.

Source specifications, a list of strings in `mr.developer <https://pypi.python.org/pypi/mr.developer>`_ sources format. If you specify plone_sources, the ``mr.developer`` extension will be used with auto-checkout set to ``*`` and git_clone_depth set to ``1``.

Private repository source present a special challenge. The typical solution will be to set up a repository user with the ssh public key for the ``plone_buildout`` user.


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


plone_install_zeoserver
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_install_zeoserver: no

Allows you to turn on and off the creation of a zeoserver. Defaults to ``yes``. Useful if the zeoserver is not on the same machine as the clients.


plone_zeo_ip
~~~~~~~~~~~~

.. code-block:: yaml

    plone_zeo_ip: 192.168.1.100

The ip address for the Zope database server. Defaults to ``127.0.0.1``. Useful if the zeoserver is not on the same machine as the clients.


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

Extra text to add to all the client buildout parts. Defaults to ``""``.
Don't use this to add ``zope-conf-additional`` stanzas, as they may be overridden.


plone_client1_extras
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_client1_extras: |
        webdav-address = 9080
        ftp-address = 8021

Extra text to add to only the first client buildout part. Defaults to ``""``.
Don't use this to add ``zope-conf-additional`` stanzas, as they may be overridden.


plone_zeo_extras
~~~~~~~~~~~~~~~~

Extra text to add to the ZEO server part of the buildout.


plone_zope_conf_additional
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_zope_conf_additional: |
        <product-config foobar>
            spam eggs
        </product-config>

Use this directive to add a ``zope-conf-additional`` section to client zope configurations.


plone_client_tcpcheck
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_client_tcpcheck: off

As of ``ansible.plone_server`` role version 1.3.0, we use ``five.z2monitor`` to set up monitor threads for each Plone ZEO client.
You may use this directive to turn this off.
Default is ``on``.


plone_client_base_tcpcheck_port
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_client_base_tcpcheck_port: 7200

If ``plone_client_tcpcheck`` is ``on``, monitor threads will be configured for each Plone ZEO client.
This directive allows you to control the base port.
There will be as many ports used as there are Plone ZEO clients.
The default is ``{{ plone_client_base_port + 100 }}``.
This is not a global variable; it may only be overridden in the ``plone_config`` argument when the role is called.


plone_extra_parts
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_extra_parts:
      zopepy: |
        recipe = zc.recipe.egg
        eggs = ${buildout:eggs}
        interpreter = zopepy
        scripts = zopepy
      diazotools: |
        recipe = zc.recipe.egg
        eggs = diazo

Extra parts to add to the automatically generated buildout. These should be in a key/value format with the key being the part name and the value being the text of the part. Defaults to ``{}``.


plone_buildout_extra
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_buildout_extra: |
      allow-picked-versions = false
      socket-timeout = 5

Allows you to add settings to the automatically generated buildout. Any text specified this way is inserted at the end of the ``[buildout]`` part and before any of the other parts. Defaults to empty.

Use this variable to add or override controlling settings to buildout. If you need to add parts, use ``plone_extra_parts`` for better maintainability.


plone_buildout_extra_dir
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_buildout_extra_dir: local_path

Copies a local directory or the *contents* of a directory into the buildout directory on the remote server.

Use this variable to drop extra files (or even subdirectories) into the buildout directory. Local path may be absolute or relative to the playbook directory. Put a ``/`` on the end of the local path if you wish to copy the contents of the directory. Leave off the trailing ``/`` to copy the directory itself.

If the copied files change, buildout will be run if ``plone_autorun_buildout`` is ``true`` (the default). However, the autorun mechanism is not able to detect any other kind of change. For example, if you've used this setting, then remove it, the autorun will not be triggered.


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

The full local (host) filepath of a buildout egg cache. Defaults to ``none``. Should not be used at the same time as ``plone_buildout_cache_url``.


plone_create_site
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_create_site: no

Should we create a Plone site in the ZODB when it's first initialized? Defaults to ``yes``.


plone_site_id
~~~~~~~~~~~~~

.. code-block:: yaml

    plone_site_id: client55

If we're creating a Plone site, what should the id be? Defaults to ``Plone``.


plone_extension_profiles
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_extension_profiles:
        - jarn.jsi18n:default

List additional Plone profiles which should be activated in the new Plone site.  These are only activated if the ``plone_create_site`` variable is set. Defaults to empty.


plone_default_language
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_default_language: es

If we're creating a Plone site, what should be the default language? Defaults to ``en``.


supervisor_instance_discriminator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    supervisor_instance_discriminator: customer_15

Optionally use this variable when you're installing multiple plone servers on the same machine.
The value for ``supervisor_instance_discriminator`` will be set as a prefix to all supervisor jobs for this Plone server.

You do not need to set a ``supervisor_instance_discriminator`` if the servers have different instance names.


plone_download_requirements_txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_download_requirements_txt: yes

Should we download a ``requirements.txt`` file from ``dist.plone.org`` for the matching version of Plone?
If you set this to ``no``, or if ``dist.plone.org`` does not have a requirements file for the target version, we'll create one from a template.
If we create from template, the following settings are used, all of which may be overridden:

.. code-block:: yaml

    plone_setuptools_version: '26.1.1'
    plone_zc_buildout_version: '2.5.3'
    plone_pip_version: '10.0.1'

However the ``requirements.txt`` file is created, it will be used via pip to prime our virtual environment.


plone_restart_after_buildout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_restart_after_buildout: yes

When set to ``yes`` (the default), the role will restart the clients that are running under supervisor whenever buildout runs. This may be undesirable in situations where uptime is a high priority and clients are slow to start serving requests.

The full Plone Ansible Playbook has a nice alternative in such cases: a restart script that removes clients from the load-balancer cluster and doesn't return them until after priming caches.


Cron jobs
~~~~~~~~~

plone_pack_at
~~~~~~~~~~~~~

.. code-block:: yaml

    plone_pack_at:
      minute: 30
      hour: 1
      weekday: 7

When do you wish to run the ZEO pack operation? Specify minute, hour, and weekday specifications for a valid *cron* time. See ``CRONTAB(5)``. Defaults to 1:30 Sunday morning. Set to ``no`` to avoid creation of a cron job.


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

When do you wish to run the backup operation?  Specify minute, hour, and weekday specifications for a valid *cron* time. See ``CRONTAB(5)``. Defaults to 2:30 every morning.  Set to ``no`` to avoid creation of a cron job.


plone_keep_backups
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_keep_backups: 3

How many generations of full backups do you wish to keep? Defaults to ``2``.

.. note::

    Daily backups are typically partial: they cover the differences between the current state and the state at the last full backup. However, backups after a pack operation are complete (full) backups -- not incremental ones. Thus, keeping two full backups means that you have backups for ``plone_keep_backups * days_between_packs`` days. See the `collective.recipe.backup documentation <https://pypi.python.org/pypi/collective.recipe.backup>`_.


plone_keep_blob_days
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_keep_blob_days: 21

How many days of blob backups do you wish to keep? This is typically set to ``keep_backups * days_between_packs`` days. Default is ``14``.


plone_backup_path
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_backup_path: /mnt/backup/plone

Where do you want to put your backups? The destination must be writable by the ``plone_daemon`` user. Defaults to ``./var`` inside your buildout directory. Subdirectories are created for blob and filestorage backups.


plone_rsync_backup_options
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    plone_rsync_backup_options: --perms --chmod=ug+rx

Rsync options set within the backup scripts (see `collective.recipe.backup <https://pypi.python.org/pypi/collective.recipe.backup#supported-options>`_). This can be used, for example, to change permissions on backups so they can be downloaded more easily. Defaults to empty.
