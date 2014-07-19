#!/usr/bin/python

#
# IMPORTS
#
import os
import tempfile
import time
import sys

#
# CONSTANTS
#
CREATE_LOOP="losetup %(loop)s %(image)s"
KPARTX="kpartx -a %(loop)s"
MOUNT="mount %(loop)s%(partition)s %(mount_dir)s"


#
# CODE
#
def mountImage(imagePath, rootPartition):
    """
    Mounts a qemu image

    @type  imagePath: str
    @param imagePath: path to image

    @type  rootPartition: str
    @param rootPartition: root partition, ex: p1

    @rtype: dict
    @returns: mount directory and loop device
    """
    # image not exist: skip
    if not os.path.exists(imagePath):
        print "Image %s does not exists" % imagePath
        sys.exit(1)

    # create loop device associated to image
    loopDev = findLoopDevice()
    os.system(CREATE_LOOP % {"loop":loopDev, "image":imagePath})

    # run kpartx and mount
    tmpdir =  tempfile.mkdtemp()
    os.system(KPARTX % {"loop":loopDev})

    # wait loop device to be ready
    time.sleep(1)
    os.system(MOUNT % {"loop":loopDev.replace("/dev","/dev/mapper"), 
                       "mount_dir":tmpdir,
                       "partition": rootPartition}) 
    
    return {"dir":tmpdir, "loop":loopDev}
# mountImage

def findLoopDevice():
    """
    Find available loop device

    @rtype: str
    @returns: loop path
    """
    return os.popen("losetup -f").read().replace("\n","")
# findLoopDevice

def sedFile(strOriginal, strFinal, file):
    """
    Change string in a file

    @type  strOriginal: str
    @param strOriginal: string to be changed

    @type  strFinal: str
    @param strFinal: string to belong

    @type  file: str
    @param file: file path

    @rtype: None
    @returns: Nothing
    """
    recordFile(readFile(file).replace(strOriginal, strFinal), file)
# sedFile

def readFile(file):
    """
    Reads file

    @type  file: str
    @param file: file path

    @rtype: str
    @returns: file content
    """
    # verify file
    if not os.path.exists(file):
        print "File %s does not exists" % file
        sys.exit(1)

    # read file
    fd = open(file, "r")
    content = fd.read()
    fd.close()

    return content
# readFile

def recordFile(content, file):
    """
    Reads file

    @type  content: str
    @param content: file content

    @type  file: str
    @param file: file path

    @rtype: str
    @returns: file content
    """
    # read file
    fd = open(file, "w")
    fd.write(content)
    fd.close()
# recordFile
