Requirements
------------

Target server
^^^^^^^^^^^^^

Supported platforms
```````````````````

At the moment, we are testing with Ubuntu 14 (Trusty) LTS, Ubuntu 15 (Vivid), Ubuntu 16 (Xenial) LTS, Debian wheezy, Debian jessy, and CentOS 7.

The following components are currently not supported for the CentOS environment:

- ``jnv.unattended-upgrades``
- ``tersmitten.fail2ban``

This means that installation of unattended upgrades and the fail2ban service do not occur on CentOS.

SSH access; sudo
````````````````

Beyond the basic platform, the only requirements are that you have ``ssh`` access to the remote server with full ``sudo`` rights.

For local testing via a virtual machine, any machine that supports VirtualBox/Vagrant should be adequate.

Potential Problems
``````````````````

Problems may arise from insufficient memory or disk space when running the playbook on the target server.
This section describes some common problems and their symptoms, helping you to recognize them and decide how to handle them.

When running the playbook for the first time on a server that has less than 1GB of RAM and has insufficient disk swap space, then you will encounter an error message like the following.

.. code-block:: console

    TASK [plone.plone_server : Run buildout - output goes to /usr/local/plone-5.0/zeoserver/buildout.log] ******************************************************
    fatal: [myhost.com]: FAILED! => {"changed": true, "cmd": "bin/buildout > buildout.log 2>&1", "delta": "0:00:17.152622", "end": "2017-05-21 22:29:38.031577", "failed": true, "rc": 1, "start": "2017-05-21 22:29:20.878955", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}
            to retry, use: --limit @/Users/myusername/projects/myproject/ansible-playbook/playbook.retry

Noting that the output of buildout is located on the target machine in ``/usr/local/plone-5.0/zeoserver/buildout.log``, we can see what happened.

.. code-block:: console

    Getting distribution for 'lxml==3.5.0'.
    x86_64-linux-gnu-gcc: internal compiler error: Killed (program cc1)
    Please submit a full bug report,
    with preprocessed source if appropriate.
    See <file:///usr/share/doc/gcc-4.8/README.Bugs> for instructions.
    Building lxml version 3.5.0.
    Building without Cython.
    Using build configuration of libxslt 1.1.28
    Compile failed: command 'x86_64-linux-gnu-gcc' failed with exit status 4
    error: Setup script exited with error: command 'x86_64-linux-gnu-gcc' failed with exit status 4
    An error occurred when trying to install lxml 3.5.0. Look above this message for any errors that were output by easy_install.
    While:
      Installing client1.
      Getting distribution for 'lxml==3.5.0'.
    Error: Couldn't install: lxml 3.5.0

lxml could not be installed.

To remedy this situation, there are several options depending on the hosting provider, each of which impacts financial cost, labor, maintenance, and hardware, and other users.

How to Resolve Insufficient Resources on Digital Ocean
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Create a droplet with at least 1GB of RAM.
* Create a droplet with 512GB of RAM, then resize it up to 1GB temporarily in Digital Ocean's interface without changing the disk size. Run the playbook to install lxml, then downsize the droplet back to 512GB of RAM.
* Create a swap disk. Digital Ocean provides instructions for doing this on `Ubuntu 16 <https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04>`_ and other distributions, but also warns that "[d]oing so can impact the reliability of the underlying hardware for you and your neighbors."

Local setup
^^^^^^^^^^^

On your local machine (the one from which you're controlling the remote server), you will need a recent copy of Ansible. `docs.ansible.com <http://docs.ansible.com/intro_installation.html>`_ has thorough installation instructions. We will be testing with release versions of Ansible, so don't feel a need to track Ansible development. (Note: don't us your OS package manager to install Ansible; you may get an unusable out-of-date version.)

Ansible's only dependency is a recent version of Python 2.6 or later.

You will also nearly certainly want git, both for cloning the playbook and for version-controlling your own work.

To clone the stable branch of the playbook, use the command:

.. code-block:: bash

    git clone https://github.com/plone/ansible-playbook.git -b STABLE

Quick setup
^^^^^^^^^^^

If you're using a machine with the following installed:

- Python 2.7
- virtualenv 2.7
- make

you may install quickly by cloning the playbook and using the commands:

.. code-block:: bash

    git clone https://github.com/plone/ansible-playbook.git -b STABLE
    cd ansible-playbook
    make all

This will install Ansible in the ``ansible-playbook`` directory via virtualenv and install role requirements.

Use ``bin/ansible-playbook`` in place of ``ansible-playbook`` to run your playbook.

Ansible role requirements
^^^^^^^^^^^^^^^^^^^^^^^^^

We have a few Ansible role dependencies which you may fulfill via Ansible Galaxy with the command:

.. code-block:: bash

    ansible-galaxy -r requirements.yml -p roles install

This should be executed in your playbook directory. Downloaded requirements will be dropped into the ``roles`` directory there.

Remote setup
^^^^^^^^^^^^

Ansible requires that the target server have a recent Python 2.x on the server. Newer platforms (like Ubuntu Xenial and later) may not have this activated on pristine new machines.

If you get connection errors from Ansible, check the remote machine to make sure Python 2.7 is available.
``which python2.7`` will let you know.
If it's missing, use your package manager to install it.

On Ubuntu Xenial (16.0.4 LTS), ``sudo apt-get install -y python`` will do the trick.
