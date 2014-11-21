Introduction
------------

Plone's Ansible Playbook can completely provision a remote server to run a full-stack, production-ready Plone server, including:

* Plone in a cluster configuration;

* Automatic starting and process control of the Plone cluster with `supervisor <http://supervisord.org>`_;

* Load balancing of the cluster with `HAProxy <http://www.haproxy.org/>`_;

* Caching with `Varnish <https://www.varnish-cache.org/>`_;

* `Nginx <http://wiki.nginx.org/Main>`_ as a world-facing remote proxy and URL rewrite engine;

* An outgoing-mail-only mail server using `Postfix <http://www.postfix.org/>`_;

* Monitoring and log analysis with `munin-node <http://munin-monitoring.org/>`_ and `logwatch <http://linuxcommand.org/man_pages/logwatch8.html>`_, `fail2ban <http://www.fail2ban.org/wiki/index.php/Main_Page>`_.

* Use of a local `VirtualBox <https://www.virtualbox.org/>`_ provisioned via `vagrant <https://www.vagrantup.com/>`_ to test and model your remote server.

An Ansible playbook and roles describe the desired condition of the server. The playbook is used both for initial provisioning and for updating.

.. note ::

    If you want to take more control of your playbook, the `Plone server role <https://github.com/plone/ansible.plone_server>`_ is available by itself, and is listed on `Ansible Galaxy <https://galaxy.ansible.com/list#/roles/2212>`_.

TL;DR
^^^^^

1. Install a current version of Ansible;

2. If you wish to test locally, install Vagrant and VirtualBox;

3. Check out or download a copy of this package;

4. Run ``ansible-galaxy -p roles -r requirements.txt install`` to install required roles;

5. Edit ``configure.yml`` to override settings; create and edit ``local-configure.yml`` if you don't wish to change parts of the distribution;

6. To test in a local virtual machine, run ``vagrant up`` or ``vagrant provision``;

7. To deploy, create an Ansible inventory file for the remote host and run ``ansible-playbook --ask-sudo-pass -i myhost playbook.yml``;

8. Set a real password for your Plone instance on the target server;

9. Set up appropriate firewalls.


Automated-server provisioning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal of an automated-server provisioning system like Ansible is a completely reproducible server configuration. If you wish to achieve this goal, discipline yourself to never changing configuration on your target machines via login.

That doesn't mean you never log in to your provisioned server. It just means that when you do, you resist changing configuration options directly. Instead, change your playbook, test your changes against a test server, then use your playbook to update the target server.

We chose Ansible for our provisioning tool because:

1. It requires no client component on the remote machine. Everything is done via ssh.

2) It's YAML configuration files use structure and syntax that will be familiar to Python programmers. YAML basically represents a Python data structure in an outline. Conditional and loop expressions are in Python. Templating via Jinja2 is simple and clean.

3) `Ansible's documentation <http://docs.ansible.com>` is excellent and complete.

4) Ansible is easily extended by roles. Many basic roles are available on `Ansible Galaxy <http://galaxy.ansible.com>`_.

Provisioning a Plone server
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The stack
`````````

It's easy to `install Plone on a laptop or desktop <http://docs.plone.org/manage/installing/index.html>`_ for testing, development, theming and evaluation. Installing Plone for production, particularly for a busy or complex site is harder, and requires you learn about a variety of moving parts:

* ZEO server
* ZEO clients
* Process-control
* Load balancing
* Reverse-proxy caching
* URL rewriting and HTTPS support including certificate management

If any of this is new to you, spend some time with the `Guide to deploying and installing Plone in production <http://docs.plone.org/manage/deploying/index.html>`_ before continuing.

What about other apps?
``````````````````````

This playbook assumes that your target server will be pretty much devoted to Plone's stack. If that doesn't match your plans, then feel free to pick and choose among the roles that have been created and gathered to make up this playbook. Then use them and others to create your own.

Major choices
^^^^^^^^^^^^^

Your production-server requirements may vary widely. Perhaps the biggest variable is the number of logged-in users you wish to support. You may serve thousands of complex pages per second -- if they are not customized per user -- on the lightest of servers. On the other hand, if you expect to serve 100 pages per second of content that is customized per user, you'll need one or more powerful servers, and will spend serious analysis time optimizing them.

This playbook is trying to help you out at both extremes -- and in-between. To meet these varied needs requires that you make some important configuration choices. Fortunately, you're not stuck with them! If a server configuration doesn't meet your needs, scale up your server power and edit your playbook configuration.

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

    git clone https://github.com/plone/ansible-playbook.git

Picking up required roles
`````````````````````````

*Roles* are packages of Ansible settings and tasks. The Plone Playbook has separate roles for each of the major components it works with. These roles are not included with the playbook itself, but they are easy to install.

To install the required roles, issue the command ``ansible-galaxy -p roles -r requirements.txt install`` from the playbook directory. This will create a roles subdirectory and fill it with the required roles.

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

.. warning ::

    If you did not change the ``plone_initial_password`` variable, then you new site may be managed from the Zope/Plone root via the default password. *Fix this.*

Hotfixes, Updates, Upgrades
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning ::

    If you are administering an Internet-accessible Plone install, you **must** subscribe to the `Plone-Announce mailing list <https://lists.sourceforge.net/lists/listinfo/plone-announce>`_ to receive vital security and version update announcements. Expect to apply periodic hotfixes to maintain your site.

This is the **minimum** responsibility of a site administrator. Ideally you should also participate in the Plone community and read other Plone news.