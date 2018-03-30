#!/usr/bin/python3

import hashlib
from uuid import getnode
import os

mac=str(hex(getnode()))
#mac = '0xb827ebf04609'

print(mac)
