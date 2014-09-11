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
BASENAME="debian"
INTERFACES_CONFIG="""
auto eth3
iface eth3 inet static
    address %(ip)s
    netmask 255.255.255.224
    gateway 143.106.167.129
    dns-nameservers 8.8.8.8
"""
DISK=os.path.join(os.getcwd(), "disks/debian.qcow2")
ROOT_PARTITION="p2"
TEMPLATE="debian.xml"

#
# CODE
#
def createDebian(key):
    """
    Creates debian host

    @type key: string
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

    # allow password authentication on ssh
    utils.sedFile("without-password", "yes", os.path.join(mntDir, "etc/ssh/sshd_config"))

    # print ip used
    print "IP: " + IP[mac]
    print "root password: 60fb619414782814d344e9a08d77101ce31057fec58f35643ad167cf67c5e128ea66c750d08282633bb432619c146e0543ae8d61b885902b9f61302b537aaf07"
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

