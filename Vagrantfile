# -*- mode: ruby -*-
# vi: set ft=ruby :


$script = <<SCRIPT
    # Install system requirements
    apt-get update -y
    apt-get install -y git python2.7 python-pip python2.7-dev imagemagick python3-pip
    pip install -r /vagrant/requirements.txt
    pip install tox
    pip3 install -r /vagrant/requirements.txt
    pip3 install tox
SCRIPT

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-i386-vagrant-disk1.box"
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.provision "shell", inline: $script

end