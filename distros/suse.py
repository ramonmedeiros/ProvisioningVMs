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
from commom import IP

import commom
import crypt
import hashlib
import re
import utils

#
# CONSTANTS
#
BASENAME="suse"
DISK=os.path.join(os.getcwd(), "disks/suse.img")
ROOT_PARTITION="p3"
TEMPLATE="suse.xml"

#
# CODE
#
def createSuse(key):
    """
    Creates suse host

    @type  key: str
    @param key: public key

    @rtype: None
    @returns: Nothing
    """
    # create VM
    commom.createVM(BASENAME, DISK, editFiles, ROOT_PARTITION, TEMPLATE, key)
# createFedora

def editFiles(mntDir, name, mac):
    """
    Edit files on image

    @type  mntDir: str
    @param mntDir: mount dir of the VM disk

    @type  name: str
    @param name: vm name

    @type  mac: str
    @param mac: mac address

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
    netconfig = os.path.join(mntDir, "etc/sysconfig/network/ifcfg-eth0")
    content = utils.readFile(netconfig)
    bootproto = re.search("BOOTPROTO=.*",content).group(0)
    if "dhcp" not in bootproto:
        utils.sedFile(bootproto, "BOOTPROTO=dhcp", netconfig)

    # print ip used
    print "IP: " + IP[mac]
    print "root password: 39af21a2ac52f3d5d0df3400c78342b2af80010e0bf3eb5d9e4a9fb931f0ea13904019853568d66d8428265e43e1d237339fda6f9056cc8eca8a582734e3ee8c"
    commom.printSSHPort(mntDir)
    # read shadow
    #shadow = os.path.join(mntDir, "etc/shadow")
    #content = utils.readFile(shadow)

    # parse old password and salt
    #oldpasswd = re.search("root:.*?:", content).group(0)
    #oldsalt = re.search("\\$.*\\$", oldpasswd).group(0)
    
    # print new password
    #passwd = hashlib.md5(os.urandom(1)).hexdigest()

    #print "Root Password will be %s" % passwd
    #newpasswd = crypt.crypt("passwd", oldsalt)
    #utils.sedFile(oldpasswd, "root:%s:" % newpasswd, shadow)
# editFiles

