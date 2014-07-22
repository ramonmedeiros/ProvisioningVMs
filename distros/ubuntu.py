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
BASENAME="ubuntu"
INTERFACES_CONFIG="""
auto eth0
iface eth0 inet static
    address %(ip)s
    netmask 255.255.255.224
    gateway 143.106.167.129
"""
DISK=os.path.join(os.getcwd(), "disks/ubuntu.img")
IP = {
"4c:45:42:45:cd:01":"143.106.167.131",
"4c:45:42:45:cd:02":"143.106.167.132",
"4c:45:42:45:cd:03":"143.106.167.133",
"4c:45:42:45:cd:04":"143.106.167.134",
"4c:45:42:45:cd:05":"143.106.167.135",
"4c:45:42:45:cd:06":"143.106.167.136",
"4c:45:42:45:cd:07":"143.106.167.137",
"4c:45:42:45:cd:08":"143.106.167.138",
"4c:45:42:45:cd:09":"143.106.167.139",
"4c:45:42:45:cd:0a":"143.106.167.140",
"4c:45:42:45:cd:0b":"143.106.167.141"
}
RESOLV_CONF="nameserver 8.8.8.8"
ROOT_PARTITION="p2"


#
# CODE
#
def createUbuntu():
    """
    Creates ubuntu host

    @rtype: None
    @returns: Nothing
    """
    # create VM
    commom.createVM(BASENAME, DISK, editFiles, ROOT_PARTITION)
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

