# * vim: ft=ruby *

require 'yaml'
CONFIG_FILE = 'ansible/group_vars/vagrant.yml'
parms = YAML::load File.open(CONFIG_FILE)

Vagrant.configure("2") do |config|
  config.vm.box     = 'debian7'
  config.vm.box_url = 'http://puppet-vagrant-boxes.puppetlabs.com/debian-70rc1-x64-vbox4210.box'

  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory",  1024]
    v.customize ["modifyvm", :id, "--usb",     "on"]
    v.customize ["modifyvm", :id, "--usbehci", "on"]
  end

  config.vm.synced_folder '.', parms["app_path"]
  config.vm.network :private_network, ip: "192.168.33.72"
  config.vm.network :forwarded_port, guest: 7002, host: 7002

  config.vm.provision :ansible do |ansible|
    ansible.playbook = 'ansible/vagrant.yml'
    ansible.inventory_path = 'ansible/hosts'
    ansible.limit = 'vagrant'
    ansible.host_key_checking = false
    ansible.sudo = true
    ansible.extra_vars = { ansible_ssh_user: 'vagrant' }
  end
#  config.vm.provision :shell,
#                      :path => 'install/vagrant_bootstrap.sh',
#                      :args => [ parms["APP_PATH"] ]
end
