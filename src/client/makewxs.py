#!/usr/bin/env python
from elementtree import ElementTree
import buildlib
import sys
import os
import re

version = buildlib.getVersion()

tree = ElementTree.parse(sys.argv[1])
oldversion = tree.getroot().getchildren()[0].attrib['Version']
print "Setting WIX script version to %s from  %s" %(version, oldversion)
tree.getroot().getchildren()[0].attrib['Version'] = version
print "Adding dist files to WIX script"

main = tree.getroot().getchildren()[0].getchildren()[3].getchildren()[2].getchildren()[0].getchildren()[0]
dir = os.listdir('dist')
for file in dir:
    
    attr = dict()
    pair = os.path.splitext(file)
    base = pair[0]
    ext = pair[1]
    if len(base) > 8:
        short = base[0:8] + ext
        attr['LongName'] = file
    else:
        short = base + ext
    attr['Id'] = short
    attr['DiskId'] = '1'
    attr['Name'] = short
    attr['src'] = 'dist/' + file
    attr['Vital'] = 'yes'
    fileElement = ElementTree.Element('ns0:File', attr)
    
    #creates short cut for application
    if ".exe" in short and short != 'w9xpopen.exe':
        shortcuts = [["%s_prg_lnk", 'ProgramMenuDir' ],
                    [ "%s_dsk_lnk", 'DesktopFolder' ] ]
        fancyName = base.replace("_", " ")        
        for id_lnk, directory in  shortcuts :
            shortAttr = { 
            'Id': (id_lnk % base),
            'Directory': directory, 
            'Name':short,
            'LongName':fancyName,
            'WorkingDirectory':"INSTALLDIR",
            'IconIndex':"0" }
            fileElement.append(ElementTree.Element('ns0:Shortcut', shortAttr))
                               
    main.append(fileElement)

tree.write(sys.argv[1].split('.')[0] + '-build.wxs')
