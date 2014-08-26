nova-lxc-contrail-vif-driver
============================

OpenStack Nova VIF driver for OpenContrail to be used with LXC as hypervisor.

Edit your ```/etc/nova/nova.conf```:
```
[libvirt]
vif_driver=nova_lxc_contrail_vif.contrailvif.VRouterVIFDriver
virt_type=lxc
```

Troubleshooting
---------------

If nova is not able to mount your image, you have to edit
```/usr/lib/python2.7/dist-packages/nova/virt/disk/api.py``` as well.
```
380     img = _DiskImage(image=image, use_cow=use_cow, mount_dir=container_dir, partition=1)
```

```_DiskImage``` by default, does not try to mount the first partition. But
those cloud-images, I tried, do contain one partition. However, with this
change, nova depends on an image containing one partition with the system
installed into. Without this change, nova depends on an image without any
partition. The system has to be installed into this image directly.
