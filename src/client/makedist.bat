setup.py py2exe -c
cd dist
ren logparsegui.exe "Everquest Log Parser.exe"
rem copy %windir%\system32\msvcp71.dll .
copy %windir%\sysWOW64\msvcp71.dll .
cd ..

