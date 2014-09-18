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

The Configuration File
^^^^^^^^^^^^^^^^^^^^^^

System options
``````````````

Plone options
`````````````

Load-balancer options
`````````````````````

Caching proxy options
`````````````````````

Web-server options
``````````````````

Virtual hosting setup
`````````````````````

Testing with Vagrant
--------------------

virtualbox configuration

targetting the virtualbox

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