#!/usr/bin/env python
import sys
from os.path import dirname, abspath
PROJECT_ROOT=abspath(dirname(__file__))
sys.path.insert(0,PROJECT_ROOT)
print "PROJECT_ROOT: %s" %(PROJECT_ROOT,)

import os, sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gamestats.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
