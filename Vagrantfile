# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.network "forwarded_port", guest: 80, host: 1080
  config.vm.network "forwarded_port", guest: 1080, host: 2080
  config.vm.network "forwarded_port", guest: 6081, host: 7081
  config.vm.network "forwarded_port", guest: 8080, host: 9080
  config.vm.network "forwarded_port", guest: 4949, host: 5949

  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 1
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
  end

  config.vm.define "trusty", primary: true do |myhost|
      myhost.vm.box = "ubuntu/trusty32"
  end

  config.vm.define "vivid", autostart: false do |myhost|
      myhost.vm.box = "ubuntu/vivid64"
  end

  config.vm.define "wheezy", autostart: false do |myhost|
      myhost.vm.box = "debian/wheezy64"
  end

  config.vm.define "jessie", autostart: false do |myhost|
      myhost.vm.box = "debian/jessie64"
  end


end
