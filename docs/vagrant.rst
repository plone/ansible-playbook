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


