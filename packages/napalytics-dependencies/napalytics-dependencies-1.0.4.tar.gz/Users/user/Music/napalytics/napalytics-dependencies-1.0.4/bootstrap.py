
import os
import subprocess
import sys
pathstring=os.path.dirname(os.path.realpath(__file__))
packages=pathstring+"\\"+"packages"
sys.path.append(packages)
import requirements
