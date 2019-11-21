Testing the Playbook with Vagrant
---------------------------------

Instead of testing your playbook by applying it on your target deployment machine, you can test your playbook locally using Vagrant. 

Vagrant includes an Ansible provisioner and will run the playbook when you first run ``vagrant up`` and again when you run ``vagrant provision``.

While Vagrant knows about Ansible, and the playbook specification is in your VagrantFile, you still must have Ansible itself available.

If you've installed Ansible globally, no other steps are necessary. If you wish to use a virtual environment to contain your Ansible installation, it's a little more work to get going:

.. code-block:: bash

    cd ansible.playbook
    virtualenv ./
    bin/pip install ansible
    vagrant up

If you wish to run ``ansible-playbook`` directly with the command:

.. code-block:: bash

    bin/ansible-playbook -i vbox_host.cfg playbook.yml

``vbox_host.cfg`` is automatically generated when vagrant provisions the host server.

Common errors
-------------

ssh stores host keys and checks them every time you try to reconnect to the same address.
Since your Vagrant installs are always at the same host and port (``127.0.0.1:2222``), you will receive ``SSH Error: Host key verification failed while connecting to 127.0.0.1:2222`` error messages each time you install and connect with a new virtual box.

To resolve these errors, use the command:

.. code-block:: bash

    ssh-keygen -f "~/.ssh/known_hosts" -R [127.0.0.1]:2222

to remove the old host key, then try again.

This should not happen if you're using the generated ``vbox_host.cfg``, as it turns off Ansible's host key checking.

Using the Vagrant
-----------------

To use your Vagrant, you must use SSH. 

Vagrant maps host ports into the guest VirtualBox OS. 

The standard mapping takes host port ``2222`` to the guest's SSH port, ``22``.

To SSH to your Vagrant:

.. code-block:: bash

    vagrant ssh

Port Mapping
------------

Vagrant maps host ports into the guest VirtualBox OS. The standard mapping takes host port ``2222`` to the guest's SSH port, ``22``.

The Vagrantfile included with this kit maps several more ports. The general rule is to map each guest port to a host port ``1000`` higher:

.. code-block:: console

  config.vm.network "forwarded_port", guest: 80, host: 1080
  config.vm.network "forwarded_port", guest: 1080, host: 2080
  config.vm.network "forwarded_port", guest: 4949, host: 5949
  config.vm.network "forwarded_port", guest: 6081, host: 7081
  config.vm.network "forwarded_port", guest: 8080, host: 9080

You can find these forwarded port settings by opening VirtualBox, selecting your Vagrant (will be called something like ``ansible-playbook``), right-clicking, choosing :guilabel:`Settings`, clicking :guilabel:`Network`, expanding the :guilabel:`Advanced` widget, and clicking the button :guilabel:`Port Forwarding`.

Here is what the forwarded ports are used for and where they are defined:

- 80, 443: nginx (``roles/nginx/templates/host.j2``)
- 1080: haproxy (``roles/haproxy/defaults/main.yml``)
- 4949: munin_node (``roles/munin-node/defaults/main.yml``)
- 6081: varnish (``roles/varnish/defaults/main.yml``)
- 8100: zeo_port (``roles/plone.plone_server/defaults/main.yml``)
- 8081: client_base_port (``roles/plone.plone_server/defaults/main.yml``)

Note that when you use host port ``1080`` to connect to guest port ``80``, the virtual hosting will not work correctly. You'll get the homepage, but links -- including those to stylesheets and JavaScript resources, will be wrong. So, you can't really test virtual host rewriting via Vagrant.
