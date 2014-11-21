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

