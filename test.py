# -*- coding: utf-8 -*

import os

rootFilePath = "/Users/wcy/workspace/"
for root, dirs, files in os.walk(rootFilePath):
    print(root)
    print(dirs)
    print(files)
