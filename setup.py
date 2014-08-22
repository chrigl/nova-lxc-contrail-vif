#
# Copyright (c) 2014, Christoph Glaubitz. Some rights reserved.
#
from setuptools import setup

setup(
    name='nova_lxc_contrail_vif',
    version='0.1dev',
    packages=['nova_lxc_contrail_vif'],
    zip_safe=False,
    install_requires=['nova_contrail_vif'],
    long_description='Contrail nova vif plugin for lxc',
)
