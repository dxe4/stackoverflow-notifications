#!/usr/bin/env python3
#decided not to go for zip because of QIcon(accepts path but not file, but may find a way to deal with it)
import os
import zipfile

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        for file in files:
            zip.write(os.path.join(root, file), os.path.basename(file))

if __name__ == '__main__':
    zip = zipfile.ZipFile('sonot.zip', 'w')
    zipdir(os.path.dirname(os.path.realpath(__file__)), zip)
    zip.close()