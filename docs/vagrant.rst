Testing with Vagrant
--------------------

This is really easy. Vagrant includes an Ansible provisioner and will run the playbook when you first run ``vagrant up`` and again when you run ``vagrant provisions``.

While Vagrant knows about Ansible, and the playbook specification is in your VagrantFile, you still must have Ansible itself available.

If you've installed Ansible globally, no other steps are necessary. If you wish to use a virtualenv to contain your Ansible installation, it's a little more work to get going:

.. code-block:: bash

    cd ansible.playbook
    virtualenv ./
    bin/pip install ansible
    bin/pip install ansible-vagrant
    vagrant up

    bin/ansible-playbook-vagrant playbook.yml


Testing
-------

Vagrant maps host ports into the guest VirtualBox OS. The standard mapping takes host port 2222 to the guest's SSH port, 22.

The Vagrantfile included with this kit maps several more ports. The general rule is to map each guest port to a host port 1000 higher:

  config.vm.network "forwarded_port", guest: 80, host: 1080
  config.vm.network "forwarded_port", guest: 1080, host: 2080
  config.vm.network "forwarded_port", guest: 6081, host: 7081
  config.vm.network "forwarded_port", guest: 8080, host: 9080
  config.vm.network "forwarded_port", guest: 4949, host: 5949

The hardest of these to test will be the guest port 80, as it will be travelling through virtual host mapping, and generally won't work well for Plone testing.