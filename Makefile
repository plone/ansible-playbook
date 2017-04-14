help :
	@echo "usage: make all";
	@echo
	@echo "Installs a virtualenv environment and sets up ansible in the virtualenv."
	@echo ""
	@echo "Requires Python 2.7 dev, virtualenv-2.7 and build-essential tools."
	@echo ""
	@echo "After install, use bin/ansible-playbook or activate virtualenv."
	@echo ""

all : bin/ansible roles/plone.plone_server

roles/plone.plone_server : | bin/ansible
	bin/ansible-galaxy install -p roles -r requirements.yml --ignore-errors

bin/ansible : | bin
	bin/pip install -U ansible

bin :
	virtualenv -p python2.7 .
