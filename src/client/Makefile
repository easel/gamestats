# This is the make file for eqlogdb
#
# Dependencies:
# 	Win32 Unix Environment (UnxUtils)
# 	WinSVN 1.3
# 	Python 2.3 + win32all + wxPython + libxml2
# 
#*/
MAKE=make
include basic.mk
export prefix:=$(shell pwd)

.PHONY:	default
default: clean installer

.PHONY: installer
installer:	eqlogdb.msi

.PHONY:	update
update:
	$(SVN) update

.PHONY:	commit
commit:
	$(SVN) commit

.PHONY:	status
status:
	$(SVN) status

.PHONY:	clean
clean:
	-$(DEL) /s *.~*
	-$(DEL) /s *~
	-$(DEL) /s *.log
	-$(DEL) .\#*
	-$(DEL) .pyc
	-$(DEL) .pyd
	-$(DEL) ChangeLog ChangeLog.xml

dist/lpgui.exe:	*.py 
	cmd /c setup.py py2exe
	-$(COPY) C:\WINDOWS\sysWOW64\msvcp71.dll dist

ChangeLog.xml:	*.py Makefile *.py
	cmd /c svn log -v --xml > $@

ChangeLog:	ChangeLog.xml
	cmd /c svn2log.py $< 

version-build.ini: version.ini ChangeLog
	cmd /c updateversion.py

eqlogdb-build.wxs:  eqlogdb.wxs dist/lpgui.exe version-build.ini
	cmd /c makewxs.py eqlogdb.wxs

eqlogdb.wixobj:     eqlogdb-build.wixobj
	$(COPY) $< $@

