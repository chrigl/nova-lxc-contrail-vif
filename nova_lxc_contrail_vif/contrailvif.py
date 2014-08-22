import logging
import gettext

gettext.install('contrial_vif')

from nova_contrail_vif.contrailvif import VRouterVIFDriver as VRouterVIFDriverBase
from nova.network import linux_net
from nova.virt.libvirt import designer
from nova.virt.libvirt.vif import LibvirtBaseVIFDriver
#from nova_contrail_vif.contrailvif import *

LOG = logging.getLogger(__name__)

class VRouterVIFDriver(VRouterVIFDriverBase):
    """VIF driver for VRouter when running Quantum and Lxc as hypervisor."""

    @staticmethod
    def _get_br_name(dev):
        return 'br%s' % dev[3:]

    def get_config(self, instance, vif, image_meta, inst_type):
        #conf = super(VRouterVIFDriver, self).get_config(instance, vif, image_meta, inst_type)
        conf = LibvirtBaseVIFDriver.get_config(self, instance, vif, image_meta, inst_type)
        dev = self.get_vif_devname(vif)
        br_name = self._get_br_name(dev)
        designer.set_vif_host_backend_bridge_config(conf, br_name)
        designer.set_vif_bandwidth_config(conf, inst_type)

        return conf

    def plug(self, instance, vif):
        iface_id = vif['id']
        dev = self.get_vif_devname(vif)
        linux_net.create_tap_dev(dev)

        br_name = self._get_br_name(dev)

        linux_net.LinuxBridgeInterfaceDriver.ensure_bridge(br_name, dev)
        linux_net._execute('ip', 'link', 'set', br_name, 'promisc', 'on', run_as_root=True)

        # port_id(tuuid), instance_id(tuuid), tap_name(string), 
        # ip_address(string), vn_id(tuuid)
        import socket
        from nova_contrail_vif.gen_py.instance_service import ttypes
        port = ttypes.Port(self._convert_to_bl(iface_id), 
                           self._convert_to_bl(instance['uuid']), 
                           br_name, 
                           vif['network']['subnets'][0]['ips'][0]['address'],
                           self._convert_to_bl(vif['network']['id']),
                           vif['address'],
                           instance['display_name'],
                           instance['hostname'],
                           instance['host'],
                           self._convert_to_bl(instance['project_id']))

        self._agent_inform(port, iface_id, True)

    def unplug(self, instance, vif):
        """Unplug the VIF from the network by deleting the port from
        the bridge."""
        LOG.debug(_('Unplug'))
        iface_id = vif['id']
        dev = self.get_vif_devname(vif)
        br_name = self._get_br_name(dev)

        import socket
        from nova_contrail_vif.gen_py.instance_service import ttypes
        port = ttypes.Port(self._convert_to_bl(iface_id), 
                           self._convert_to_bl(instance['uuid']), 
                           dev, 
                           vif['network']['subnets'][0]['ips'][0]['address'],
                           self._convert_to_bl(vif['network']['id']),
                           vif['address'],
                           instance['display_name'],
                           instance['hostname'],
                           instance['host'],
                           self._convert_to_bl(instance['project_id']))

        self._agent_inform(port, iface_id, False)
        linux_net.LinuxBridgeInterfaceDriver.remove_bridge(br_name)
        linux_net.delete_net_dev(dev)
