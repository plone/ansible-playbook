======================
Plone Ansible playbook
======================

.. admonition:: Description

    Using Ansible to provision a Plone server

    This document is currently an experiment in specification by documentation.

.. contents:: :local:

Introduction
------------

Plone's Ansible Playbook can completely provision a remote cloud server to run the full stack of Plone, including:

* Plone in a cluster configuration;

* Automatic starting and process control of the Plone cluster with `supervisor <http://supervisord.org>`_;

* Load balancing of the cluster with `HAProxy <http://www.haproxy.org/>`_;

* Caching with `Varnish <https://www.varnish-cache.org/>`_;

* `Nginx <http://wiki.nginx.org/Main>`_ or `Apache <http://httpd.apache.org/>`_ as a world-facing remote proxy and URL rewrite engine;

* An outgoing-mail-only mail server using `Postfix <http://www.postfix.org/>`_;

* Monitoring and log analysis with `munin-node <http://munin-monitoring.org/>`_ and `logwatch <http://linuxcommand.org/man_pages/logwatch8.html>`_.

TL;DR
^^^^^

1. Install a current version of Ansible;

2. If you wish to test locally, install Vagrant and VirtualBox;

3. Check out or download a copy of this package;

4. Run ``ansible-galaxy requirements.yml`` to install required roles;

5. Edit ``configure.yml`` to override settings;

6. To test in a local virtual machine, run ``vagrant up``;

7. To deploy, create an Ansible inventory file for the remote host and run ``ansible-playbook -i myhost playbook.yml``;

8. Set a real password for your Plone instance on the target server;

9. Set up appropriate firewalls.

Automated server provisioning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Provisioning a Plone server
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The stack
`````````

ZEO server, ZEO clients, supervisor, haproxy, varnish, apache or nginx

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

passwordless sudo

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

System options
``````````````

admin_email

motd

auto_upgrades

additional_packages

Plone options
`````````````
target

buildout_git_repo

..note:

    If you use your own buildout from a repository, you still need to specify your client count so that the playbook can 1) set up the supervisor specifications to start/stop and monitor clients, and 2) set up the load balancer.

    Client part names must follow the pattern `client#` where # is a number (1,2,3 ...). Client ports must be numbered sequentially beginning with 8081 or the value you set for client_base_port. The zeoserver part must be named `zeoserver` and be at 8100 or the value you set for zeo_port.

initial_password

client_count

client_memory_profile

client_max_memory

additional_eggs

additional_versions

    appends to version list

zeo_port

client_base_port

autorun_buildout=(yes|no)


Load-balancer options
`````````````````````

install_loadbalancer

loadbalancer_port

monitor_port

monitor_password

Caching proxy options
`````````````````````

install_proxycache

proxycache_port

Web-server options
``````````````````

install_webserver

Virtual hosting setup
~~~~~~~~~~~~~~~~~~~~~

.. codeblock:: yaml

    virtual_hosts: [
        {'hostname': xxx, 'zodb_path': xxx, 'port': xxx,}
        ]

(certificate file handling!)

Mail-server options
```````````````````

install_mailserver

mailserver_forward

Monitoring options
``````````````````

install_muninnode

muninnode_allowed_ips

install_logwatch

Remember munin supervisor monitor

fail2ban
check nginx logs for login attempts

logwatch?

Testing with Vagrant
--------------------

virtualbox configuration

targetting the virtualbox

Testing
-------

Do tests when appropriate to connect to ports both from outside and inside

Live host deployment
--------------------

Creating a host file
^^^^^^^^^^^^^^^^^^^^


Updating
^^^^^^^^

Using tags for quick, partial updates

Remaining issues
----------------

Firewall
^^^^^^^^

Passwords
^^^^^^^^^

Hotfixes, Updates, Upgrades

Subscribe to XXX for security announcements