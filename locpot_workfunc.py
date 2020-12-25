#!/usr/bin/env python
## Original algorithm: Byungdeok Yu <ybd@uos.ac.kr>
## PYTHON VERSION reduck and yangd5d5
import sys, math, string, re, numpy
usage = ‘Usage: %s inputfile(LOCPOT) FermiEnergy(option) \n’ % sys.argv[0]
usage = usage + ‘If you do not insert the FermiEnergy, write just average values. \n’
usage = usage + ‘If you input the FermiEnergy, values consider Fermi Energy \n’
foottext = ‘\n## Thank you \n## Jinwoo Park <reduck96@physics.uos.ac.kr> \n## Lanhee Yang <yangd5d5@physics.uos.ac.kr>’
version = 20090224

## PRINT COPYRIGHT
print “## LOCPOT - Workfunction x-y plot convert for VASP”
print “## Version %s \n” % version

# Check option

FermiE = 0.0 # Initialize Fermi Energy
if len(sys.argv) == 1:
  print usage
  print foottext
  sys.exit(1)

if len(sys.argv) == 2:
  infilename = sys.argv[1]
  print ‘Do not consider Fermi Energy\n’

if len(sys.argv) == 3:
  infilename = sys.argv[1]
  FermiE = float(sys.argv[2])
  print ‘Inserted Fermi Energy: %f \n’ % FermiE

#try:
# infilename = sys.argv[1]
# except:

# print usage
# print foottext
# sys.exit(1)

# Done Check option

# FILE CHECK --
try:
  ifile = open(infilename, ‘r’) # open file for reading
except:
  print ‘---- WARNING! WRONG FILE NAME ---- \n---- CHECK YOUR LOCPOT FILE ----\n’
  print foottext
  sys.exit(1)

# read and print comment line
print ‘Subject: ‘+ ifile.readline()

# Jump primitive vector configuration
for i in range(4):
  ifile.readline()

# Read Number of kind of atoms and read numbers each other
ReadNumberOfKindOfAtoms = ifile.readline().split()
NumberOfKindOfAtoms = len(ReadNumberOfKindOfAtoms)

# Sum total number of atoms
TotalNumberOfAtoms = 0
for i in range(NumberOfKindOfAtoms):
  TotalNumberOfAtoms = TotalNumberOfAtoms +
int(ReadNumberOfKindOfAtoms[i])
# debug print TotalNumberOfAtoms
# Jump comment(dummy - Cartesian? or Direct?)
ifile.readline()

for i in range(TotalNumberOfAtoms):
  ifile.readline()

#Jump Comment(dummy blank line)
ifile.readline()

#Read number of X/Y/Z elements
NumberOfElements = ifile.readline().split()

#NumberOfElements[0]: number of X-axis elements
#NumberOfElements[1]: number of Y-axis elements
#NumberOfElements[2]: number of Z-axis elements
NX = int(NumberOfElements[0])
NY = int(NumberOfElements[1])
NZ = int(NumberOfElements[2])

# debug -- print NX, NY, NZ
print “Matrix: %d x %d x %d (X, Y, Z)” % (NX, NY, NZ)
# empty array for DATA[NX, NY, NZ]
DATA=numpy.zeros((NX, NY, NZ),float)

## WHILE LOOP
## Outmost NZ / Middle NY / INNER NX
x=0; y=0; z=0; i=0;
line = ifile.readline().split() # read first line
count = len(line)

while z<NZ:
  while y<NY:
    while x<NX:
      if count == 0:
        line = ifile.readline().split()
        count = len(line)
        i=0
        DATA[x,y,z]=float(line[i])
# debug print ‘DATA[%d,%d,%d] = %f’ % (x,y,z, DATA[x, y,z])
      count=count-1
      i = i+1
      x = x+1
      y=y+1
      x=0
    z=z+1
    y=0

## DONE READ DATA

## take average of x-axis values
x=0; y=0; z=0;
XAVR=numpy.zeros((NY, NZ),float) # 2D array
while z<NZ:
  while y<NY:
    while x<NX:
      XAVR[y,z] = XAVR[y,z] + DATA[x,y,z]
        x=x+1
      XAVR[y,z] = XAVR[y,z]/float(NX)
      y=y+1
      x=0
    z=z+1
    y=0

## take average of y-axis values
y=0; z=0;
AVR=numpy.zeros((NZ),float) # 1D array
while z<NZ:
  while y<NY:
    AVR[z] = AVR[z] + XAVR[y,z]
    y=y+1
# AVR[z] = AVR[z]/float(NZ) 20090224> fix NZ->NY, Thanks Prof. Yu
  AVR[z] = AVR[z]/float(NY)
  z=z+1
  y=0

### CHECK
#z=0;
#while z<NZ:
# print ‘%d %f’ % (z, AVR[z])
# z=z+1
#
# FILE WRITE
outfile = open(“output.dat”,”w”)
for i in range(0,NZ):
  inputtext =’%d %f \n’ % (i, AVR[i]-float(FermiE))
  outfile.write(inputtext)
outfile.close()

print ‘--> RESULT FILE: output.dat\n’

############################################################
# print foot-text
print foottext

# file close
ifile.close()

### Copyright - see http://spcc.uos.ac.kr/copyright
### SPCC, University of Seoul
