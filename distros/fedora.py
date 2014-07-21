#!/usr/bin/python

#
# PATH
#
import os
import sys
sys.path.append(os.getcwd())

#
# IMPORTS
#
import commom
import crypt
import re
import utils

#
# CONSTANTS
#
BASENAME="fedora"
DISK=os.path.join(os.getcwd(), "disks/fedora.img")
ROOT_PARTITION="p5"

#
# CODE
#
def createFedora():
    """
    Creates fedora host

    @rtype: None
    @returns: Nothing
    """
    # create VM
    commom.createVM(BASENAME, DISK, editFiles, ROOT_PARTITION)
# createFedora

def editFiles(mntDir, name):
    """
    Edit files on image

    @type  mntDir: str
    @param mntDir: mount dir of the VM disk

    @type  name: str
    @param name: vm name

    @rtype: None
    @returns: Nothing
    """
    # change hostname
    hostname = os.path.join(mntDir, "etc/hostname")
    utils.recordFile(name, hostname)

    # set network as dhcp
    netconfig = os.path.join(mntDir, "etc/sysconfig/network-scripts/ifcfg-eth0")
    content = utils.readFile(netconfig)
    bootproto = re.search("BOOTPROTO=.*",content).group(0)
    if "dhcp" not in bootproto:
        utils.sedFile(bootproto, "BOOTPROTO=dhcp", netconfig)

    # change root password
    shadow = os.path.join(mntDir, "etc/shadow")
    content = utils.readFile(shadow)
    oldpasswd = re.search("root:.*?:", content).group(0)
    newpasswd = crypt.crypt("senhaboa", crypt.mksalt())
    utils.sedFile(oldpasswd, newpasswd, shadow)
# editFiles

