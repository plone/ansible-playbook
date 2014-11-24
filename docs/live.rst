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

    If you did not change the ``plone_initial_password`` variable, then your new site may be managed from the Zope/Plone root via the default password. *Fix this.*

Hotfixes, Updates, Upgrades
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning ::

    If you are administering an Internet-accessible Plone install, you **must** subscribe to the `Plone-Announce mailing list <https://lists.sourceforge.net/lists/listinfo/plone-announce>`_ to receive vital security and version update announcements. Expect to apply periodic hotfixes to maintain your site.

This is the **minimum** responsibility of a site administrator. Ideally you should also participate in the Plone community and read other Plone news.
