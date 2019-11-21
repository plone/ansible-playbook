Setting up the Playbook
^^^^^^^^^^^^^^^^^^^^^^^

Clone or fork-and-clone
```````````````````````

Take a few moments to think about how you're going to customize the Plone Playbook. Are you likely to make substantial changes? Or simply change the option settings?

If you expect to make substantial changes, you'll want to create your own git fork of the Plone Playbook. Then, clone your branch. That way you'll be able to push changes back to your branch. We assume that you either know how to use git, or will learn, so we won't try to document this usage.

If you expect to change only option settings, then just clone the Plone Playbook to your local computer (not the target server):

.. code-block:: bash

    git clone https://github.com/plone/ansible-playbook.git -b STABLE

Note that this clone is from the ``STABLE`` branch. That's likely what you want unless your helping with development. ``master`` is the development branch.

Picking up required roles
`````````````````````````

*Roles* are packages of Ansible settings and tasks. The Plone Playbook has separate roles for each of the major components it works with. These roles are not included with the playbook itself, but they are easy to install.

To install the required roles, issue the command ``ansible-galaxy -p roles -r requirements.yml install`` from the playbook directory. This will create a roles subdirectory and fill it with the required roles.

If you want to store your roles elsewhere, edit the ``ansible.cfg`` file in the playbook directory.


Customizing the deployment
^^^^^^^^^^^^^^^^^^^^^^^^^^

There are three major strategies for customization: forking, a local configuration file and Ansible inventory variables.

**If you are working on your own fork**, it's yours. You may set variables inside the playbook.

**If you cloned or downloaded the master distribution**, you will probably want to avoid changing the files from the distribution. That would make it hard to update. Instead, create a new file ``local-configure.yml`` and put your custom option specifications in it. This file will not be overridden when you pull an update from the master.

For a quick start, copy one of the ``sample*.yml`` files to ``local-configure.yml``, then customize.

Using the local configuration strategy, add only the options you wish to change to ``local-configure.yml``. Edit them there.

Ansible inventory variables
```````````````````````````

Ansible allows you to set variables for particular hosts or groups of hosts. Check the Ansible documentation on `Inventory variables <http://docs.ansible.com/ansible/intro_inventory.html>`_ for details. This is a particularly good approach if you are hoping to support multiple hosts, as different variables may be set for different hosts.

If you use inventory variables, note that any variable you set in ``local-configure.yml`` will override your inventory variables.

Inventory variables are not as practical for use with Vagrant if you're using ``vagrant up`` to provision. Instead, use ``vagrant up --no-provision`` to bring up the box, then use ``ansible-playbook`` to provision.

Customizing buildout configuration
``````````````````````````````````
Plone is typically installed using `buildout <http://www.buildout.org/en/latest/>`_ to manage Python dependencies. Plone's Ansible Playbook uses operating-system package managers to manage system-level dependencies and uses buildout to manage Python-package dependencies.

Buildout cofiguration files are nearly always customized to meet the need of the particular Plone installation. At a minimum, the buildout configuration details Plone add ons for the install. It is nearly always additionally customized to meet performance and integration requirements.

You have two available mechanisms for doing this customization in conjunction with Ansible:

* You may rely on the buildout skeleton supplied by this playbook. It will allow you to set values for commonly changed options like the egg (Python package) list, ports and cluster client count.

* You may supply a git repository specification, including branch or tag, for a buildout directory skeleton. The Plone Ansible Playbook will clone this or pull updates as necessary.

If you choose the git repository strategy, your buildout skeleton must, at a minimum, include a buildout file ``.cfg`` file. Use ``plone_buildout_cfg`` to set the filename if it's not ``live.cfg``. It will also commonly contain a ``src/`` subdirectory and extra configuration files. It will probably **not** contain ``bin/``, ``var/`` or ``parts/`` directories. Those will typically be excluded in your ``.gitignore`` file.

.. note::

    See the ``plone_buildout_git_repo`` variable documentation in the Plone Options chapter.

If you use a buildout directory checkout, you must still specify in your Playbook variables the names and listening port numbers of any client parts you wish included in the load balancer configuration. Also specify the name of your ZEO server part if it is not ``zeoserver``.

A sample strategy
`````````````````

The Plone Community's administrative infrastructue team maintains several several servers using the Ansible Playbook. Here's our strategy:

* Fork the Plone Ansible Playbook. Because we wish to keep some administrative details confidential, our fork is in a private repository.

* To your fork, add an ``inventory.cfg`` file. This file contains the host names, IP addresses and SSH variables specific to each of our hosts.

* Create a `./host_vars` directory. This directory contains a ``.yml`` file with a name matching the host name in ``inventory.cfg``. Each file contains the equivalent of ``local-configure.yml``, but for a particular host:

  .. code-block:: text

      ansible-playbook/host_vars/
          plone.com.yml
          ploneconf.yml
          plone.org.yml

* Create a ``vbox_inventory.cfg`` file containing VirtualBox setup for each host you wish to test via Vagrant/VirtualBox.

* Commit all your new files and push to your fork repository.

* Never change any of the files that you inherited from the master Plone Ansible Playbook.

* When you want to update **all** your hosts, use a command like:

  .. code-block:: bash

      ansible-playbook -K playbook.yml

* To update **a particular** host, use a command like:

  .. code-block:: bash

      ansible-playbook -K -l plone.com playbook.yml

The ``-l`` flag allows you to run a playbook on a single host, using the host name from ``inventory.cfg``.

* Picking up changes from the Plone Ansible Playbook

Add the Plone Ansible Playbook to your clone as a remote:

.. code-block:: bash

    git remote add papb https://github.com/plone/ansible-playbook.git

Now, on your clone, do the following:

.. code-block:: bash

    git checkout master   # check out your own master branch
    git fetch papb        # fetch refs from the Plone Ansible Playbook
    git merge papb/STABLE # merge changes from the Plone Ansible Playbook

Resolve conflicts if any. Commit and push to your fork repo.


The Configuration File
^^^^^^^^^^^^^^^^^^^^^^

The configuration file format is YAML with Jinja2 templating. It's well-documented at `docs.ansible.com <http://docs.ansible.com/YAMLSyntax.html>`_.
