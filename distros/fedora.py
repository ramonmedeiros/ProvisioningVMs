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
import hashlib
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
    print "Image Editing\n\n"
    
    print "Changing hostname"
    hostname = os.path.join(mntDir, "etc/hostname")
    utils.recordFile(name, hostname)

    # set network as dhcp
    print "Set network as DHCP"
    netconfig = os.path.join(mntDir, "etc/sysconfig/network-scripts/ifcfg-eth0")
    content = utils.readFile(netconfig)
    bootproto = re.search("BOOTPROTO=.*",content).group(0)
    if "dhcp" not in bootproto:
        utils.sedFile(bootproto, "BOOTPROTO=dhcp", netconfig)

    # read shadow
    shadow = os.path.join(mntDir, "etc/shadow")
    content = utils.readFile(shadow)

    # parse old password and salt
    oldpasswd = re.search("root:.*?:", content).group(0)
    oldsalt = re.search("\\$.*\\$", oldpasswd).group(0)
    
    # print new password
    passwd = hashlib.md5(os.urandom(1)).hexdigest()

    print "Root Password will be %s" % passwd
    newpasswd = crypt.crypt("passwd", oldsalt)
    utils.sedFile(oldpasswd, "root:%s:" % newpasswd, shadow)
# editFiles

