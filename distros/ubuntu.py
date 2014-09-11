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
BASENAME="ubuntu"
INTERFACES_CONFIG="""
auto eth1
iface eth1 inet dhcp
"""
DISK=os.path.join(os.getcwd(), "disks/ubuntu.img")
RESOLV_CONF="nameserver 8.8.8.8"
ROOT_PARTITION="p2"
TEMPLATE="ubuntu.xml"

#
# CODE
#
def createUbuntu(key):
    """
    Creates ubuntu host

    @type  key: str
    @param key: public key

    @rtype: None
    @returns: Nothing
    """
    # create VM
    commom.createVM(BASENAME, DISK, editFiles, ROOT_PARTITION, TEMPLATE, key)
# createUbuntu

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
    print "Set network as static"
    netconfig = os.path.join(mntDir, "etc/network/interfaces")
    fd = open(netconfig, "a")
    fd.write("\n" + INTERFACES_CONFIG % {"ip":IP[mac]})
    fd.close()

    # set dns server
    dnsconfig = os.path.join(mntDir, "etc/resolvconf/resolv.conf.d/tail")
    if not os.path.exists(os.path.dirname(dnsconfig)):
        os.makedirs(os.path.dirname(dnsconfig))
    fd = open(dnsconfig, "w")
    fd.write("\n" + RESOLV_CONF)
    fd.close()

    # print ip used
    print "IP " + IP[mac]
    print "Default password for root is 481a91e7a60caabd7af6f2ff019d774cfe93376244d46c6347078ea37245890a74dfd6b1559496742b3d117079796e974e858f7a10a216218e1ebc7afc0ea16c"

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

