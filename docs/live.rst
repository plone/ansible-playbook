Live host deployment
--------------------

Creating a host file
^^^^^^^^^^^^^^^^^^^^

You'll need to tell Ansible how to connect to your host. There are multiple ways to do this. The easiest for our purposes is to create a *manifest* file.

Create a file with a name like ``myhost.cfg`` that follows the pattern:

.. code-block:: ini

    plone.com ansible_ssh_user=stevem ansible_ssh_host=192.168.1.50 ansible_ssh_port=5555

You may leave off the ``ansible_ssh_host`` setting if the hostname is real. However, when doing early provisioning, it's often not available. ``ansible_ssh_port`` is only required if you want to use a non-standard ssh port. ``ansible_ssh_user`` should be the login id on the remote machine. That user must have sudo rights.

Running your playbook
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    ansible-playbook --ask-sudo-pass -i myhost.cfg playbook.yml

The ``--ask-sudo-pass`` option instructs Ansible to ask for your user password when it uses sudo for provisioning. It's not required if the remote user has password-less sudo rights.

Updating
^^^^^^^^

Using tags for quick, partial updates.

The following tags are set up in playbook.yml.

- plone
- haproxy
- varnish
- postfix
- logwatch
- munin
- motd
- nginx

When you use one of these tags while running your playbook, only the bare minimum setup and the module named will be updated.

Apply a tag using the ``--tags`` option. Example: ``--tags="nginx"``


Firewall
^^^^^^^^

The main playbook, ``playbook.yml``, does **not** configure your firewall.

A separate playbook, ``firewall.yml`` sets up a basic firewall that closes all ports except ssh, http and https. The munin-node port is also opened to your monitoring server(s).

.. note::

    To reach other ports, use SSH tunnelling. In the default setup, you will have to use a tunnel and connect to the load-balancer port in order to get access to the Zope root. (The default proxy-cache setup blocks http basic authentication.)


Passwords
^^^^^^^^^

You must set the ``plone_initial_password`` variable to the desired password for the Zope ``admin`` user. Use this id only for initial Plone login, then create users within Plone.

Hotfixes, Updates, Upgrades
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

    If you are administering an Internet-accessible Plone install, you **must** subscribe to the `Plone-Announce mailing list <https://lists.sourceforge.net/lists/listinfo/plone-announce>`_ to receive vital security and version update announcements. Expect to apply periodic hotfixes to maintain your site.

This is the **minimum** responsibility of a site administrator. Ideally you should also participate in the Plone community and read other Plone news.
