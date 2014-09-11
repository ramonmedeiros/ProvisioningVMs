#!/usr/bin/python

#
# PATH
#
import sys
import os
#sys.path.append(os.getcwd())


#
# IMPORTS
#
import re
import tempfile
import utils


#
# CONSTANTS
#
AUTOSTART="virsh autostart %s &>/dev/null"
DEFINE_VM="virsh define %s &>/dev/null"
LIBVIRT_IMAGES="/var/lib/libvirt/images/"
LIBVIRT_MACS="grep -o -E \"..:..:..:..:..:..\" /etc/libvirt/qemu/*xml 2> /dev/null"
LIST_MACHINES="virsh list --all"
START_VM="virsh start %s &>/dev/null"
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
"4c:45:42:45:cd:0b":"143.106.167.141",
"4c:45:42:45:cd:0c":"143.106.167.151",
"4c:45:42:45:cd:0d":"143.106.167.152",
"4c:45:42:45:cd:0e":"143.106.167.153",
"4c:45:42:45:ce:01":"143.106.167.154",
"4c:45:42:45:ce:02":"143.106.167.155",
"4c:45:42:45:ce:03":"143.106.167.156",
"4c:45:42:45:ce:04":"143.106.167.157"
}

#
# CODE
#
def cleanUpMount(loopDev, mntDir):
    """
    Clean up qemu image mount

    @type  loopDev: str
    @param loopDev: loop device

    @type  mntDir: str
    @param mntDir: mount directory

    @rtype: None
    @returns: Nothing
    """
    print "Cleaning up"
    
    # umount and remove xml file
    os.system("umount " + mntDir)

    # qcow2
    if "nbd" in loopDev:
        os.system("qemu-nbd -d " + loopDev)
        return

    # remove mapper device
    os.system("dmsetup remove %s*" % loopDev.replace("/dev","/dev/mapper"))
    os.system("losetup -d %s" % loopDev)
# cleanUpMount

def createLibvirtXML(name, mac, img, template):
    """
    Creates, define and start VM XML
    
    @type  name: str
    @param name: vm name

    @type  mac: str
    @param mac: mac address of the new VM

    @type  img: str
    @param img: img path

    @type  template: str
    @param template: template name

    @rtype: None
    @returns: Nothing
    """
    # fill xml file
    template = os.path.join(os.getcwd(), "distros/", template)
    newXML = utils.readFile(template)
    newXML = newXML % {"name": name,
                       "disk_path": img,
                       "mac_address": mac
    }

    # write xml file
    tmpfile =  tempfile.mkstemp()[1]
    utils.recordFile(newXML, tmpfile)

    # define vm
    print "Defining new VM %s" % name
    if 0 != os.system(DEFINE_VM % tmpfile):
        print "Cannot define %s" % tmpfile
        sys.exit(1)
    os.system("rm -f %s" % tmpfile)

    # start vm
    os.system(START_VM % name)
    os.system(AUTOSTART % name)

# createLibvirtXML

def createVM(basename, disk, editFiles, rootPartition, template, key):
    """
    Edit VM disk, create libvirt entry and start each

    @type  basename: str
    @param basename: vm basename

    @type  disk: str
    @param disk: disk path

    @type  editFiles: function
    @param editFiles: function to edit VM conf files

    @type  rootPartition: str
    @param rootPartition: root partition

    @type  template: str
    @param template: template name

    @type  key: str
    @param key: public key

    @rtype: None
    @returns: Nothing
    """
    # get name and mac
    name = findAvailableName(basename)
    mac = findAvailableMac()
    
    # no mac available: finish
    if mac == None:
        print "No IP available: Abort"
        sys.exit(1)

    # cannot copy image: exit
    print "Copying new VM. Can take some minutes"
    img = os.path.join(LIBVIRT_IMAGES, name + ".img")
    if 0 != os.system("cp -a %s %s" % (disk,img)):
        print "Cannot copy image to libvirt directory"
        sys.exit(1)

    # mount image
    data = utils.mountImage(img, rootPartition)
    mntDir = data["dir"]
    loopDevice = data["loop"]

    # ssh directory does not exists: create it
    if os.path.exists(os.path.join(mntDir, "root/.ssh")) == False:
        os.mkdir(os.path.join(mntDir, "root/.ssh"))

    # register new key
    fd = open(os.path.join(mntDir, "root/.ssh/authorized_keys"), "a")
    fd.write("\n" + key + "\n")
    fd.close()

    # create VM
    createLibvirtXML(name, mac, img, template)

    # edit files in ISO
    editFiles(mntDir, name, mac)

    # clean up files
    cleanUpMount(loopDevice, mntDir)
# createVM

def printSSHPort(mntDir):
    """
    Prints ssh port

    @type  mntDir: str
    @param mntDir: dir where image is mounted

    @rtype: None
    @returns: Nothing
    """
    # display ssh info
    content = utils.readFile(os.path.join(mntDir, "etc/ssh/sshd_config"))
    reg = re.search(r"(\nPort) (?P<port>[0-9]*)", content)

    # no ssh passed: print default
    if reg == None:
        print "SSH port is 22"
    else:
        print "SSH port is %(port)s" % reg.groupdict()

# printSSHPort

def findAvailableName(basename):
    """
    Find a available name

    @type  basename: str
    @param basename: basename for vms

    @rtype: str
    @returns: vm name
    """
    for number in range(1,99):
        if basename + str(number) not in os.popen(LIST_MACHINES).read():
            return basename + str(number)
# findAvailableName

def findAvailableMac():
    """
    Find a available mac

    @rtype: str
    @returns: available mac address
    """
    for mac in IP.keys():
        if mac not in os.popen(LIBVIRT_MACS).read():
            return mac
    return None
# findAvailableMac
