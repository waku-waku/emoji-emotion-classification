#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import scipy as sp
import sys
import re

argvs = sys.argv
fileName = argvs[1]

f = open(fileName)
datas = f.readlines()
f.close()

datas = list(set(datas))

print(len(datas))
print(len(datas))

f = open(fileName, 'w')
for row in datas:
	f.write(row)
f.close()


