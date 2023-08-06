import glob
import subprocess
import os
pathstring=os.path.dirname(os.path.realpath(__file__))

print("Resolving Level 1 dependencies.....")
print("........................................")
globber=pathstring+"\\"+"level1"+"\\"+"*.whl"
globber2=pathstring+"\\"+"level1"+"\\"+"*.tar.gz"

for path in glob.glob(globber):
    subprocess.run(f'pip install {path}')

for path in glob.glob(globber2):
    subprocess.run(f'pip install {path}')
print("All Level 1 dependencies resolved....")
print("........................................")

print("Resolving Level 2 dependencies.....")
print("........................................")
globber=pathstring+"\\"+"level2"+"\\"+"*.whl"
globber2=pathstring+"\\"+"level2"+"\\"+"*.tar.gz"
for path in glob.glob(globber):
    subprocess.run(f'pip install {path}')
for path in glob.glob(globber2):
    subprocess.run(f'pip install {path}')
print("All Level 2 dependencies resolved....")
print("........................................")


print("Resolving Level 3 dependencies.....")
print("........................................")
globber=pathstring+"\\"+"level3"+"\\"+"*.whl"
globber2=pathstring+"\\"+"level3"+"\\"+"*.tar.gz"

for path in glob.glob(globber):
    subprocess.run(f'pip install {path}')

for path in glob.glob(globber2):
    subprocess.run(f'pip install {path}')
print("All Level 3 dependencies resolved....")
print("........................................")


print("Resolving Level 4 dependencies.....")
print("........................................")
globber=pathstring+"\\"+"level4"+"\\"+"*.whl"
globber2=pathstring+"\\"+"level4"+"\\"+"*.tar.gz"

for path in glob.glob(globber):
    subprocess.run(f'pip install {path}')

for path in glob.glob(globber2):
    subprocess.run(f'pip install {path}')

print("All Level 4 dependencies resolved....")
print("........................................")




print("Resolving Level 5 dependencies.....")
print("........................................")
globber2=pathstring+"\\"+"level5"+"\\"+"*.whl"
globber=pathstring+"\\"+"level5"+"\\"+"*.tar.gz"

for path in glob.glob(globber):
    subprocess.run(f'pip install {path}')

for path in glob.glob(globber2):
    subprocess.run(f'pip install {path}')
print("All Level 5 resolved....")
print("........................................")


print("Resolving level 6 dependencies.....")
print("........................................")
globber=pathstring+"\\"+"level6"+"\\"+"*.whl"
globber2=pathstring+"\\"+"level6"+"\\"+"*.tar.gz"

for path in glob.glob(globber):
    subprocess.run(f'pip install {path}')

for path in glob.glob(globber2):
    subprocess.run(f'pip install {path}')
print("All Level 6 resolved....")
print("........................................")

print("Resolving level 7 dependencies.....")
print("........................................")

globber=pathstring+"\\"+"level7"+"\\"+"*.whl"
globber2=pathstring+"\\"+"level7"+"\\"+"*.tar.gz"
for path in glob.glob(globber):
    subprocess.run(f'pip install {path}')

for path in glob.glob(globber2):
    subprocess.run(f'pip install {path}')

print("All dependencies resolved....")
print("........................................")