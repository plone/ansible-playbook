Introduction
------------

Plone's Ansible Playbook can completely provision a remote server to run a full-stack, production-ready Plone server, including:

* Compatibility with Plone 4.3.x, 5.0.x, 5.1.x and 5.2.x.
  5.2 may be set up with either Python 2.7 or 3 via the plone_python_version variable.
  Earlier Plones only work with 2.7.

* Plone in a cluster configuration;

* Automatic starting and process control of the Plone cluster with `supervisor <http://supervisord.org>`_;

* Load balancing of the cluster with `HAProxy <http://www.haproxy.org/>`_;

* Caching with `Varnish <https://www.varnish-cache.org/>`_;

* `Nginx <http://wiki.nginx.org/Main>`_ as a world-facing reverse proxy and URL rewrite engine;

* An outgoing-mail-only mail server using `Postfix <http://www.postfix.org/>`_;

* Monitoring and log analysis with `munin-node <http://munin-monitoring.org/>`_, `logwatch <http://linuxcommand.org/man_pages/logwatch8.html>`_ and `fail2ban <http://www.fail2ban.org/wiki/index.php/Main_Page>`_.

* Use of a local `VirtualBox <https://www.virtualbox.org/>`_ provisioned via `Vagrant <https://www.vagrantup.com/>`_ to test and model your remote server.

We generally support relatively current CentOS and Debian/Ubuntu environments. Versions currently supported are Ubuntu Xenial 16.0.4 LTS, Ubuntu 14 (Trusty) LTS, Ubuntu 15, Debian wheezy, Debian jessy, and CentOS 7.

An Ansible playbook and roles describe the desired condition of the server. The playbook is used both for initial provisioning and for updating.

.. note::

    If you want to take more control of your playbook, the `Plone server role <https://github.com/plone/ansible.plone_server>`_ is available by itself, and is listed on `Ansible Galaxy <https://galaxy.ansible.com/list#/roles/2212>`__.

TL;DR
^^^^^

1. Install a current version of Ansible;

2. If you wish to test locally, install Vagrant and VirtualBox;

3. Check out or download a copy of `the STABLE branch of this package <https://github.com/plone/ansible-playbook>`_;

4. Run ``ansible-galaxy -p roles -r requirements.yml install`` to install required roles;

5. Copy one of the ``sample*.yml`` files to ``local-configure.yml`` and edit as needed.

6. To test in a local virtual machine, run ``vagrant up`` or ``vagrant provision``;

7. To deploy, create an `Ansible inventory file <http://docs.plone.org/external/ansible-playbook/docs/live.html#creating-a-host-file>`_ for the remote host and run ``ansible-playbook --ask-sudo-pass -i myhost.cfg playbook.yml``;

8. Set a real password for your Plone instance on the target server;

9. Set up appropriate firewalls.

.. warning::

    **Python required:** Ansible requires that the target server have a recent Python 2.x on the server. Newer platforms (like Ubuntu Xenial and later) may not have this activated on pristine new machines.

    If you get connection errors from Ansible, check the remote machine to make sure Python 2.7 is available.
    ``which python2.7`` will let you know.
    If it's missing, use your package manager to install it.

    On Ubuntu Xenial (16.0.4 LTS), ``sudo apt-get install -y python`` will do the trick.

    **sshpass**: You may need to install ``sshpass`` on the host machine to manage sending passwords to the remote machine over ssh. ``sudo apt-get install -y sshpass`` will do the trick in the Debian universe.


Automated-server provisioning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The goal of an automated-server provisioning system like Ansible is a completely reproducible server configuration. If you wish to achieve this goal, discipline yourself to never changing configuration on your target machines via login.

That doesn't mean you never log in to your provisioned server. It just means that when you do, you resist changing configuration options directly. Instead, change your playbook, test your changes against a test server, then use your playbook to update the target server.

We chose Ansible for our provisioning tool because:

1) It requires no client component on the remote machine. Everything is done via ssh.

2) It's YAML configuration files use structure and syntax that will be familiar to Python programmers. YAML basically represents a Python data structure in an outline. Conditional and loop expressions are in Python. Templating via Jinja2 is simple and clean.

3) `Ansible's documentation <http://docs.ansible.com>`_ is excellent and complete.

4) Ansible is easily extended by roles. Many basic roles are available on `Ansible Galaxy <http://galaxy.ansible.com>`__.


If you need to log in
^^^^^^^^^^^^^^^^^^^^^

You should not need to. But if you do, you should know:

1) The Plone zeoserver and zeoclient processes should be run under the plone_daemon login; they will normally be controlled via supervisor;

2) Run buildout as plone_buildout.
