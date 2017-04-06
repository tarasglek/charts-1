# -*- mode: ruby -*-
# vim: ft=ruby


# ---- Configuration variables ----

GUI               = false # Enable/Disable GUI
RAM               = 2048   # Default memory size in MB

# Network configuration
DOMAIN            = ".dev.purestorage.com"
NETWORK           = "192.168.50."
NETMASK           = "255.255.255.0"

# Default Virtualbox .box
# See: https://wiki.debian.org/Teams/Cloud/VagrantBaseBoxes
BOX               = 'ubuntu/trusty64'

HOSTS = {
   "k8s-master" => ["4", RAM, GUI, "ubuntu/xenial64"],
   "k8s-node5" => ["5", RAM, GUI, "ubuntu/xenial64"],
  #  "k8s-node6" => ["6", RAM, GUI, "ubuntu/xenial64"],
}

# ---- Vagrant configuration ----

Vagrant.configure(2) do |config|
  HOSTS.each do | (name, cfg) |
    ipaddr_suffix, ram, gui, box = cfg
    ipaddr = NETWORK + ipaddr_suffix
    config.vm.define name do |machine|
      machine.vm.box   = box
      machine.vm.guest = :debian

      machine.vm.provider "virtualbox" do |vbox|
        vbox.gui    = gui
        vbox.memory = ram
        vbox.name = name
      end

      machine.vm.hostname = name + DOMAIN
      machine.vm.network 'private_network', ip: ipaddr, netmask: NETMASK
      machine.vm.provision :shell, path: "bootstrap.sh", args: "42", keep_color: true
    end
  end # HOSTS-each
  # if Vagrant.has_plugin?("vagrant-cachier")
  #   config.cache.scope = :box
  # end
end
