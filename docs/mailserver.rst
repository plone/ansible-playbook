Mail-server options
```````````````````

install_mailserver
~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    install_mailserver: (yes|no)

Do you want to install the Postfix mail server in a send-only configuration. Default is ``yes``.

.. note::

    If you choose not to install a mail server via this playbook, this becomes your responsibility.

Relaying
~~~~~~~~

.. code-block:: yaml

    mailserver_relayhost: smtp.sendgrid.net
    mailserver_relayport: 587
    mailserver_relayuser: yoursendgriduser
    mailserver_relaypassword: yoursendgridpassword

Sets up a mail relay. This may be required if you're using a service like Google Compute Engine that doesn't allow outgoing connections to external mailservers. Defaults to none.

mail_hostname
~~~~~~~~~~~~~

.. code-block:: yaml

    mail_hostname: www.plone.org

Use this setting if you need to set the hostname used by Postfix to something other than the hostname.
You may need to do this if the inventory hostname is the same as the hostname you're using for mail delivery.

Extras
~~~~~~

.. code-block:: yaml

    mailserver_maincf_extras: |
        ; turn off Postscript ip6 support
        inet_protocols = ipv4

Allows you to add extra entries at the end of the Postscript ``main.cf`` file.
