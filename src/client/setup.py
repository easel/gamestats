# setup.py
from distutils.core import setup
import py2exe

setup(data_files=["lpgui.xrc"], 
    console=["logparse.py"], windows=["lpgui.py"])
