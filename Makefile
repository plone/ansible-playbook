all : bin/ansible roles/plone.plone_server local-configure.yml

local-configure.yml :
	cp -i sample-medium.yml local-configure.yml

roles/plone.plone_server : | bin/ansible
	bin/ansible-galaxy install -p roles -r requirements.txt --ignore-errors

bin/ansible : | bin
	bin/pip install ansible

bin :
	virtualenv .


