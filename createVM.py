#!/usr/bin/python

#
# IMPORTS
#
from distros import ubuntu, fedora, debian, suse
import argparse


#
# CONSTANTS
#
DISTRO="distro"
KEY="key"

#
# CODE
#
def parseCommandLine():
    """
    Parses command line

    @rtype: int
    @returns: exit status
    """
    # get args
    parser = argparse.ArgumentParser()

    # set args
    parser.add_argument(DISTRO, type=str, help="distros supported: (fedora/ubuntu/debian/suse)")
    parser.add_argument(KEY, type=str, help="public key")
    
    # parse args
    args = parser.parse_args()
    
    # create fedora
    if args.distro == "fedora":
        fedora.createFedora(args.key)

    # create ubuntu
    elif args.distro == "ubuntu":
        ubuntu.createUbuntu(args.key)

    # create debian
    elif args.distro == "debian":
        debian.createDebian(args.key)
    
    # create suse
    elif args.distro == "suse":
        suse.createSuse(args.key)

    # no option given: show help
    else: 
        parser.print_help()
    
    # return success
    return 0
# parseCommandLine()

#
# ENTRY POINT
#
if __name__ == '__main__':
    
    # do main
    parseCommandLine()
