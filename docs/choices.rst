Provisioning a Plone server
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The stack
`````````

It's easy to `install Plone on a laptop or desktop <http://docs.plone.org/manage/installing/index.html>`_ for testing, development, theming and evaluation. Installing Plone for production, particularly for a busy or complex site is harder, and requires you learn about a variety of moving parts:

* ZEO server
* ZEO clients
* Process-control
* Load balancing
* Reverse-proxy caching
* URL rewriting and HTTPS support including certificate management

If any of this is new to you, spend some time with the `Guide to deploying and installing Plone in production <http://docs.plone.org/manage/deploying/index.html>`_ before continuing.

What about other apps?
``````````````````````

This playbook assumes that your target server will be pretty much devoted to Plone's stack. If that doesn't match your plans, then feel free to pick and choose among the roles that have been created and gathered to make up this playbook. Then use them and others to create your own.

Major choices
`````````````

Your production-server requirements may vary widely. Perhaps the biggest variable is the number of logged-in users you wish to support. You may serve thousands of complex pages per second -- if they are not customized per user -- on the lightest of servers. On the other hand, if you expect to serve 100 pages per second of content that is customized per user, you'll need one or more powerful servers, and will spend serious analysis time optimizing them.

This playbook is trying to help you out at both extremes -- and in-between. To meet these varied needs requires that you make some important configuration choices. Fortunately, you're not stuck with them! If a server configuration doesn't meet your needs, scale up your server power and edit your playbook configuration.

Take a look at the ``sample*.yml`` files for configuration examples. These present the most commonly changed configuration options.
