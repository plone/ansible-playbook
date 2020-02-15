Audit: Finding Leftover Files
`````````````````````````````

Unmaintained Files
~~~~~~~~~~~~~~~~~~

One problem with the Plone Ansible Playbook's current maintenance strategy is that it doesn't know how to delete unused nginx and supervisor configuration files.

This means that if you add and later delete a virtual host entry, there will be a leftover, unmaintained nginx host setup file.
If you add and later delete a Plone install, there will be a leftover, unmaintained supervisor configuration file.

The installer includes an ``audit`` role that will warn you about these leftover configuration files.
The ``audit`` role is the last run, and its warning message(s) should be visible on your console when the playbook finishes.

A warning from the audit module looks like:

.. code-block:: text

    WARNING: You have one or more files in /etc/nginx/sites-enabled that are not being maintained by the playbook: {{ unexpected_vhosts }}.

The current remedy for this sort of problem is to delete the unmaintained file and restart nginx or remove the job from supervisor via ``supervisorctl``.
