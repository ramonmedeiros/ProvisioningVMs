#!/usr/bin/python

#
# IMPORTS
#
from distros import ubuntu, fedora, debian
import argparse


#
# CONSTANTS
#
DISTRO="distro"

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
    parser.add_argument(DISTRO, type=str, help="distros supported: (fedora/ubuntu/debian)")
    
    # parse args
    args = parser.parse_args()
    
    # create fedora
    if args.distro == "fedora":
        fedora.createFedora()

    # create ubuntu
    elif args.distro == "ubuntu":
        ubuntu.createUbuntu()

    # create debian
    elif args.distro == "debian":
        debian.createDebian()
    
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
