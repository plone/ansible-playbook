======================
Plone Ansible playbook
======================

.. admonition:: Description

    Using Ansible to provision a Plone server

    This document is currently an experiment in specification by documentation.

.. contents:: :local:

Introduction
------------

Plone's Ansible Playbook can completely provision a remote server to run the full stack of Plone, including:

* Plone in a cluster configuration;

* Automatic starting and process control of the Plone cluster with `supervisor <http://supervisord.org>`_;

* Load balancing of the cluster with `HAProxy <http://www.haproxy.org/>`_;

* Caching with `Varnish <https://www.varnish-cache.org/>`_;

* `Nginx <http://wiki.nginx.org/Main>`_ or `Apache <http://httpd.apache.org/>`_ as a world-facing remote proxy and URL rewrite engine;

* An outgoing-mail-only mail server using `Postfix <http://www.postfix.org/>`_;

* Monitoring and log analysis with `munin-node <http://munin-monitoring.org/>`_ and `logwatch <http://linuxcommand.org/man_pages/logwatch8.html>`_, logwatch and `fail2ban <http://www.fail2ban.org/wiki/index.php/Main_Page>`_.

* Use of a local `VirtualBox <https://www.virtualbox.org/>`_ provisioned via `vagrant <https://www.vagrantup.com/>`_ to test and model your remote server.

An ansible playbook and roles describe the desired condition of the server. The playbook is used both for initial provisioning and for updating.

TL;DR
^^^^^

1. Install a current version of Ansible;

2. If you wish to test locally, install Vagrant and VirtualBox;

3. Check out or download a copy of this package;

4. Run ``ansible-galaxy -p roles -r requirements.txt`` to install required roles;

5. Edit ``configure.yml`` to override settings;

6. To test in a local virtual machine, run ``vagrant up``;

7. To deploy, create an Ansible inventory file for the remote host and run ``ansible-playbook --ask-sudo-pass -i myhost playbook.yml``;

8. Set a real password for your Plone instance on the target server;

9. Set up appropriate firewalls.

Automated server provisioning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Provisioning a Plone server
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The stack
`````````

ZEO server, ZEO clients, supervisor, haproxy, varnish, nginx

What about other apps?
``````````````````````

Major choices
^^^^^^^^^^^^^

Apache or Nginx
```````````````

ZEO clients
```````````

Number and memory use

Mail server issues
``````````````````

Requirements
------------

Target server
^^^^^^^^^^^^^

Supported platforms
```````````````````

SSH access
``````````

public key auth

sudo

Local setup
^^^^^^^^^^^

Python 2.#, virtualenv, git

Optional
^^^^^^^^

github account for easy branching and customizaiton

Preparing your playbook
-----------------------

Installing Ansible
^^^^^^^^^^^^^^^^^^

    virtualenv

Setting up the Playbook
^^^^^^^^^^^^^^^^^^^^^^^

Clone or branch-and-clone
`````````````````````````

Take a few moments to think about how you're going to customize the Plone Playbook. Are you likely to make substantial changes? Or simply change the option settings?

If you expect to make substantial changes, you'll want to create your own git branch of the Plone Playbook. Then, clone your branch. That way you'll be able to push changes back to your branch. We assume that you either know how to use git, or will learn, so we won't try to document this usage.

If you expect to change only option settings, then just clone the Plone Playbook to your local computer (not the target server)::

    git clone ####

Picking up required roles
`````````````````````````

*Roles* are packages of Ansible settings and tasks. The Plone Playbook has separate roles for each of the major components it works with. These roles are not included with the playbook itself, but they are easy to install.

To install the required roles, issue the command ``ansible-galaxy requirements.yml`` from the playbook directory. This will create a roles subdirectory and fill it with the required roles.

If you want to store your roles elsewhere, edit the ``ansible.cfg`` file in the playbook directory.

Customizing the deployment
^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two major strategies for customization.

**If you are working on your own branch**, it's yours. You may edit ``configure.yml`` to set options.

**If you cloned or downloaded the master distribution**, you will probably want to avoid changing the files from the distribution. That would make it hard to update. Instead, create a new file ``local-configure.yml`` and put your custom option specifications in it. This file will not be overriden when you pull an update from the master.

Using the local configuration strategy, copy from ``configure.yml`` only the options you wish to change to ``local-configure.yml``. Edit them there.

Customizing buildout configuration
``````````````````````````````````

Plone is typically installed using `buildout <http://www.buildout.org/en/latest/>`_ to manage Python dependencies. Plone's Ansible Playbook uses operating-system package managers to manage system-level dependencies and uses buildout to manage Python-package dependencies.

Buildout cofiguration files are nearly always customized to meet the need of the particular Plone installation. At a minimum, the buildout configuration details Plone add ons for the install. It is nearly always additionally customized to meet performance and integration requirements.

You have two available mechanisms for doing this customization in conjunction with Ansible:

* You may rely on the buildout skeleton supplied by this playbook. It will allow you to set values for commonly changed options like the egg (Python package) list, ports and cluster client count.

* You may supply a git repository specification, including branch or tag, for a buildout directory skeleton. The Plone Ansible Playbook will clone this or pull updates as necessary.

If you choose the git repository strategy, your buildout skeleton must, at a minimum, include ``bootstrap.py`` and ``buildout.cfg`` files. It will also commonly contain a ``src/`` subdirectory and extra configuration files. It will probably **not** contain ``bin/``, ``var/`` or ``parts/`` directories. Those will typically be excluded in your ``.gitignore`` file.

If you use a buildout directory checkout, you must still specify in your Playbook variables the names and listening port numbers of any client parts you wish included in the load balancer configuration. Also specify the name of your ZEO server part if it is not ``zeoserver``.

The Configuration File
^^^^^^^^^^^^^^^^^^^^^^

YAML

System options
``````````````

admin_email
~~~~~~~~~~~

.. code-block:: yaml

    admin_email: sysadmin@yourdomain.com

It is important that you update this setting. The admin_email address will receive system mail, some of which is vitally important.

Defaults to an invalid address. Mail will not be delivered.


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


Plone options
`````````````

target_path
~~~~~~~~~~~

.. code-block:: yaml

    target_path: /opt/plone

Sets the Plone installation directory.

Defaults to ``/usr/local/plone``


buildout_git_repo
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    buildout_git_repo: https://github.com/plone/plone.com.ansible.git
    buildout_git_version: master

``buildout_git_repo`` defaults to none (uses built-in buildout).

``buildout_git_version`` is the tag or branch. Defaults to ``master``.

.. note::

    If you use your own buildout from a repository, you still need to specify your client count so that the playbook can 1) set up the supervisor specifications to start/stop and monitor clients, and 2) set up the load balancer.

    Client part names must follow the pattern `client#` where # is a number (1,2,3 ...). Client ports must be numbered sequentially beginning with 8081 or the value you set for client_base_port. The zeoserver part must be named `zeoserver` and be at 8100 or the value you set for zeo_port.

    If you use your own buildout, all Plone settings except ``client_count``, ``client_base_port``, and ``client_max_memory`` are ignored.


plone_version
~~~~~~~~~~~~~

.. code-block:: yaml

    plone_version: 4.3.3

Which Plone version do you wish to install? This defaults to the current stable version at the time you copy or clone the playbook.

initial_password
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    initial_password: alnv%r(ybs83nt

Initial password of the Zope ``admin`` user. The initial password is used when the database is first created. Don't forget to change it.

Defaults to ``admin``


client_count
~~~~~~~~~~~~

.. code-block:: yaml

    client_count: 5

How many ZEO clients do you want to run?

Defaults to ``2``

.. note ::

    The provided buildout always creates an extra client ``client_reserve`` that is not hooked into supervisor or the load balancer. Use it for debugging, run scripts and quick testing.


zodb_cache_size
~~~~~~~~~~~~~~~

.. code-block:: yaml

    zodb_cache_size: 30000

How many objects do you wish to keep in the ZODB cache.

Defaults to ``30000``

.. Note ::

    The default configuration is *very* conservative to allow Plone to run in a minimal memory server. You will want to increase this is you have more than minimal memory.


zserver_threads
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    zserver_threads: 2

How many threads should run per server?

Defaults to ``1``


client_max_memory
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    client_max_memory: 800MB

A size (suffix-multiplied using “KB”, “MB” or “GB”) that should be considered “too much”. If any Zope/Plone process exceeds this maximum, it will be restarted. Set to ``0`` for no memory monitoring.

Defaults to ``0`` (turned off)

.. note ::

    This setting is used in configuration of the ``memmon`` monitor in supervisor: `superlance <http://superlance.readthedocs.org/en/latest>`_ plugin.


additional_eggs
~~~~~~~~~~~~~~~

.. code-block:: yaml

    additional_eggs:
        - Products.PloneFormGen
        - collective.cover
        - webcourtier.dropdownmenus

List additional Python packages (beyond Plone and the Python Imaging Library) that you want available in the Python package environment.

The default list is empty.

.. note ::

    Plone hotfixes are typically added as additional eggs.


additional_versions
~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    additional_versions:
      - "Products.PloneFormGen = 1.7.16"
      - "Products.PythonField = 1.1.3"
      - "Products.TALESField = 1.1.3"

The version pins you specify here will be added to the ``[versions]`` section of your buildout. The default list is empty.


zeo_port
~~~~~~~~

.. code-block:: yaml

    zeo_port: 6100

The port number for the Zope database server. Defaults to ``8100``.


client_base_port
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    client_base_port: 6080

The port number for your first Zope client. Subsequent client ports will be added in increments of 1. Defaults to ``8081``.

environment_vars
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    environment_vars:
        - "TZ US/Eastern"
        - "zope_i18n_allowed_languages en"

A list of environment variables you wish to set for running Plone instances.

Defaults to:

.. code-block:: yaml

    - "PYTHON_EGG_CACHE ${buildout:directory}/var/.python-eggs"


autorun_buildout
~~~~~~~~~~~~~~~~

.. code-block:: yaml

    autorun_buildout: (yes|no)

Do you wish to automatically run buildout if any of the Plone settings change? Defaults to ``yes``.


buildout_cache
~~~~~~~~~~~~~~

.. code-block:: yaml

    buildout_cache: http://dist.plone.org/4.3.4/buildout-cache.tar.bz2

The URL of a buildout egg cache. Defaults to the one for the current version of Plone.


Cron jobs
~~~~~~~~~

pack_at
~~~~~~~

.. code-block:: yaml

    pack_at:
      minute: 30
      hour: 1
      weekday: 7

When do you wish to run the ZEO pack operation? Specify minute, hour and weekday specifications for a valid *cron* time. See ``CRONTAB(5)``. Defaults to 1:30 Sunday morning. Set to ``no`` to avoid creation of a cron job.


keep_days
~~~~~~~~~

.. code-block:: yaml

    keep_days: 3

How many days of undo information do you wish to keep when you pack the database. Defaults to ``3``.


backup_at
~~~~~~~~~

.. code-block:: yaml

    backup_at:
      minute: 30
      hour: 2
      weekday: "*"

When do you wish to run the backup operation?  Specify minute, hour and weekday specifications for a valid *cron* time. See ``CRONTAB(5)``. Defaults to 2:30 every morning.  Set to ``no`` to avoid creation of a cron job.


keep_backups
~~~~~~~~~~~~

.. code-block:: yaml

    keep_backups: 3

How many generations of full backups do you wish to keep? Defaults to ``2``.

.. note ::

    Daily backups are typically partial: they cover the differences between the current state and the state at the last full backup. However backups after a pack operation are complete (full) backups -- not difference operations. Thus, keeping two full backups means that you have backups for ``keep_backups * days_between_packs`` days. See the `collective.recipe.backup documentation <https://pypi.python.org/pypi/collective.recipe.backup>`_.


keep_blob_days
~~~~~~~~~~~~~~

.. code-block:: yaml

    keep_blob_days: 21

How many days of blob backups do you wish to keep? This is typically set to `keep_backups * days_between_packs`` days. Default is ``14``.

backup_path
~~~~~~~~~~~

.. code-block:: yaml

    backup_path: /mnt/backup/plone

Where do you want to put your backups? The destination must be writable by the ``plone_daemon`` user. Defaults to ``./var`` inside your buildout directory. Subdirectories are created for blob and filestorage backups.


Load-balancer options
`````````````````````

install_loadbalancer
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_loadbalancer: (yes|no)

Do you want to use a load balancer? Defaults to ``yes``.

.. note ::

    If you decide not to use a load balancer, you will need to make sure that the ``loadbalancer_port`` setting points to your main ZEO client if you are using a proxy cache. If you are not using a proxy_cache, you must make sure that ``proxycache_port`` points to main ZEO client.

Defaults to ``yes``.

.. code-block:: yaml

    loadbalancer_port: 6080

The front-end port for the load balancer. Defaults to ``8080``.

.. note ::

    The haproxy stats page will be at ``http://localhost:1080/admin``. The administrative password is disabled on the assumption that the port will be firewalled and you will use any ssh tunnel to connect.

Caching proxy options
`````````````````````

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


Web-server options
``````````````````

.. code-block:: yaml

    install_webserver: (yes|no)

Do you want to install Nginx? Defaults to ``yes``.

.. note ::

    If you decide not to install the webserver -- which acts as a reverse proxy -- you are on your own for making sure that Plone is accessible at a well-known port.

Virtual hosting setup
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    virtual_hosts:
        - hostname: plone.org
          zodb_path: /Plone
          port: 80
          protocol: http
        - hostname: plone.org
          zodb_path: /Plone
          port: 443
          protocol: https
          certificate_file: /thiscomputer/path/mycert.crt
          key_file: /thiscomputer/path/mycert.key

Connects host names to paths in the ZODB.

Default value:

.. code-block:: yaml

    - hostname: localhost
      zodb_path: /Plone
      port: 80

.. note ::

    If you are setting up and SSL sever, you must supply certificate and key files. The files will be copied from your local machine (the one containing the playbook) to the target server. Your key file must not be encrypted or you will not be able to start the web server automatically.

.. warning ::

    Make sure that your source key file is not placed in a public location.


Mail-server options
```````````````````

install_mailserver
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_mailserver: (yes|no)

Do you want to install the Postfix mail server in a send-only configuration. Default is ``yes``.

.. note ::

    If you choose not to install a mail server via this playbook, this becomes your responsibility.

.. code-block:: yaml

    mailserver_relay::

XXX -- this one's important, but a bit of work


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


Testing with Vagrant
--------------------

This is really easy. Vagrant includes an Ansible provisioner and will run the playbook any time you use ``vagrant up``. While vagrant knows about Ansible, and the playbook specification is in your VagrantFile, you still must have Ansible itself available. The ideal thing to do is to create a Python virtualenv to the same directory and install Ansible into it.

.. code-block:: bash

    cd ansible.playbook
    virtualenv ./
    bin/pip install ansible
    bin/pip install ansible-vagrant
    vagrant up
    bin/ansible-playbook-vagrant playbook.yml


Testing
-------

Do tests when appropriate to connect to ports both from outside and inside?

Live host deployment
--------------------

Creating a host file
^^^^^^^^^^^^^^^^^^^^

You'll need to tell Ansible how to connect to your host. There are multiple ways to do this. The easiest for our purposes is to create a *manifest* file.

Create a file with a name like ``myhost.cfg`` that follows the pattern:

.. code-block:: ini

    plone.com --ansible_ssh_user=stevem ansible_ssh_host=192.168.1.50 ansible_ssh_port=5555

You may leave off the ``ansible_ssh_host`` setting if the hostname is real. However, when doing early provisioning, it's often not available. ``ansible_ssh_port`` is only required if you want to use a non-standard ssh port.

Running your playbook
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

    ansible-playbook --ask-sudo-pass -i myhost.cfg plone-playbook.yml

The ``--ask-sudo-pass`` option instructs Ansible to ask for your user password when it uses sudo for provisioning.

Updating
^^^^^^^^

Using tags for quick, partial updates

Firewall
^^^^^^^^

The main playbook, ``playbook.yml``, does **not** configure your firewall.

A separate playbook, ``firewall.yml`` sets up a basic firewall that closes all ports except ssh, http and https.

.. note ::

    If you are using munin-node, you will need to add a rule to open your munin node monitor port to your munin server.

Passwords
^^^^^^^^^

Hotfixes, Updates, Upgrades
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning ::

    If you are administering an Internet-accessible Plone install, you **must** subscribe to the `Plone-Announce mailing list <https://lists.sourceforge.net/lists/listinfo/plone-announce>`_ to receive vital security and version update announcements. Expect to apply periodic hotfixes to maintain your site.

This is the **minimum** responsibility of a site administrator. Ideally you should also participate in the Plone community and read other Plone news.