#!/usr/bin/python

import gpio
from gpio import read

print 'button=', read(95)
print 'led-G=', read(65)
print 'led-A=', read(90)
print 'led-R=', read(91)
