Requirements
------------

Target server
^^^^^^^^^^^^^

Supported platforms
```````````````````

At the moment, while the environment with the fullest support for the target server is Debian/Ubuntu, some initial support is available for CentOS.  This is simply because the expertise of the initial authors is with the .deb world. Adding RPM environments should not be difficult, but we need help. Your pull requests are welcome.

At the moment, we are testing with Ubuntu 14 (Trusty) LTS, Ubuntu 15 (Vivid) and with Debian wheezy, Debian jessy, and CentOS 7.

The following components are currently not supported for the CentOS environment:

  - ``jnv.unattended-upgrades``
  - ``tersmitten.fail2ban``
  - The ``firewall.yml`` playbook.


SSH access; sudo
````````````````

Beyond the basic platform, the only requirements are that you have ``ssh`` access to the remote server with full ``sudo`` rights.

For local testing via virtual machine, any machine that supports VirtualBox/Vagrant should be adequate.

Local setup
^^^^^^^^^^^

On your local machine (the one from which you're controlling the remote server), you will need a recent copy of Ansible. `docs.ansible.com <http://docs.ansible.com/intro_installation.html>`_ has thorough installation instructions. We will be testing with release versions of Ansible, so don't feel a need to track Ansible development. (Note: don't us your OS package manager to install Ansible; you may get an unusably out-of-date version.)

Ansible's only dependency is a recent version of Python 2.6 or later.

You will also nearly certainly want git, both for cloning the playbook and for version-controlling your own work.

To clone the master branch of the playbook, use the command:

    git clone https://github.com/plone/ansible-playbook.git

Ansible role requirements
^^^^^^^^^^^^^^^^^^^^^^^^^

We have a few Ansible role dependencies which you may fulfill via Ansible Galaxy with the command:

    ansible-galaxy -r requirements.txt -p roles install

This should be executed in your playbook directory. Downloaded requirements will be dropped into the ``roles`` directory there.
