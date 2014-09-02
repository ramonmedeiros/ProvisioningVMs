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
from debian import IP

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
TEMPLATE="fedora.xml"

#
# CODE
#
def createFedora(key):
    """
    Creates fedora host

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
    netconfig = os.path.join(mntDir, "etc/sysconfig/network-scripts/ifcfg-eth0")
    content = utils.readFile(netconfig)
    bootproto = re.search("BOOTPROTO=.*",content).group(0)
    if "dhcp" not in bootproto:
        utils.sedFile(bootproto, "BOOTPROTO=dhcp", netconfig)

    # print ip used
    print "IP " + IP[mac]
    print "Default password is 60fb619414782814d344e9a08d77101ce31057fec58f35643ad167cf67c5e128ea66c750d08282633bb432619c146e0543ae8d61b885902b9f61302b537aaf07"

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

