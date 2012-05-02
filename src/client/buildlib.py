#!/usr/bin/env python
import win32ui
import win32api
import os 
import shutil

def getVersion():
    win32ui.SetProfileFileName('./version-build.ini')
    return win32ui.GetProfileVal('Version Info Keys', 'FileVersion', '0')

def getPaddedVersion():
    (major, minor, checkin, build) = getVersion().split('.')
    major = "%02d" % int(major)
    minor = "%02d" % int(minor)
    checkin = "%05d" % int(checkin)
    build = "%04d" % int(build)
    return "%s.%s.%s.%s" %(major,minor,checkin,build)

def updateVersion():
    shutil.copyfile('version.ini', 'version-build.ini')
    win32ui.SetProfileFileName('./version-build.ini')
    version = win32ui.GetProfileVal('Version Info Keys', 'FileVersion', '0')
    (major, minor, checkin, build) = version.split('.')
    command = 'svn info' 
    # TODO: Lame try-except to handle svn 1.3.0 info output
    try:
        checkin = str(int(os.popen(command).read().split('\n')[3].split(':')[1]))
    except:
        checkin = str(int(os.popen(command).read().split('\n')[4].split(':')[1]))
    version = ".".join((major, minor, checkin, build))
    win32ui.WriteProfileVal('Version Info Keys', 'FileVersion', version)
    win32ui.WriteProfileVal('Version Info Keys', 'ProductVersion', version)
    return version

if __name__ == '__main__':
	updateVersion()
