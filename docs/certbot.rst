Certbot options
```````````````

The certbot playbook
~~~~~~~~~~~~~~~~~~~~

As a convenience, the Plone Ansible Playbook kit includes a separate
playbook that will install certbot-nginx and create certificates as necessary for specified hostnames.

The certbot playbook currently only supports Debian-family target servers.

To use the certbot playbook, edit your ``local-configure.yml`` file to add a ``certbot_hosts`` list variable containing an entry for each hostname for which you wish to get a certbot certificate:

.. code-block:: yaml

   certbot_hosts:
     - one.mcsmith.org
     - two.mcsmith.org

Run the playbook as you would the main playbook, adding whatever command-line switches you need (like ``-k`` or ``-K``):

.. code-block:: console

    ansible-playbook -k certbot.yml

This will first install ``python3-certbot-nginx`` from the certbot/certbot ppa.
Then it will create certificates as necessary for each hostname in the ``certbot_hosts`` list.
If a certificate already exists, it will not attempt addition.

Note that ``python3-certbot-nginx`` includes an auto-renewal cronjob.


Webserver support
~~~~~~~~~~~~~~~~~

When the nginx role creates a configuration file for a virtual host, it will check TLS hostnames against the ``certbot_hosts`` list.
If the hostname matches, the certbot certificate/key will be used automatically (unless you override this by specifying certificate/key files).

Certificate/key files for certbot are expected to be in ``/etc/letsencrypt/live/HOST_NAME`` or this mechanism will fail when nginx is reloaded after configuration.


Why is this a separate playbook?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As with the ``firewall.yml`` playbook, we want to encourage users to think and research before using the certbot playbook.
*Let's Encrypt* is security software and is not for everyone.
It should be used only with knowledge and deliberation and not as an autopilot choice.

Note in particular that the certbot-nginx support uses root priveleges for both certificate creation and renewal.
Some sysadmins choosing certbot may wish to set up their own creation/renewal systems to avoid this exposure.

Note that even if you never run the certbot playbook, you may still find the webserver setup support useful.
