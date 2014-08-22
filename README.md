nova-lxc-contrail-vif-driver
============================

OpenStack Nova VIF driver for OpenContrail to be used with LXC as hypervisor.

Edit your ```/etc/nova/nova.conf```:
```
[libvirt]
vif_driver=nova_lxc_contrail_vif.contrailvif.VRouterVIFDriver
virt_type=lxc
```
