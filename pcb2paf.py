#!/usr/bin/env python

#
#  pcb2paf.py
#
#  Copyright (C) 2011 Hamid Rostami
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#

import os
import sys
import shutil

# ---------------- Getting information
try:
	in_filename = sys.argv[1]
	out_filename = sys.argv[2]
except:
	print "Usage: pcb2paf input_file output_file"
	exit(1)

if os.path.exists(in_filename) is not True:
	print "Give me a existing file!"
	exit(2)

# ---------------- Open files
in_file = open(in_filename, "r")

shutil.copy('template.PcbDoc', out_filename)
out_file = open(out_filename, "a+w")


# ---------------- Read data structures
elements = {}
layers = {}

for line in in_file:
  if line.find("Element") is not -1:
    element_header = line
    temp_data = []
    for element_line in in_file:
      if element_line.find("(") is not -1:
        continue

      if element_line.find(")") is not -1:
        break;
      
      temp_data.append(element_line)
    
    elements.update( {element_header:temp_data} )
  
  if line.find("Layer") is not -1:
    layer_header = line
    temp_data = []
    for layer_line in in_file:
      if layer_line.find("(") is not -1:
        continue

      if layer_line.find(")") is not -1:
        break
      
      temp_data.append(layer_line)
    
    layers.update( {layer_header:temp_data} )

# ---------------- Draw Elements
for el in elements:
  info = el[ el.find('[')+1 : el.find(']') ]
  info = info.split(' ')
  mx = int(info[-7])
  my = int(info[-6])

  for line in elements[el]:
    if line.find('Pin') is not -1:
      line = line[ line.find('[')+1 : line.find(']') ]
      info = line.split(' ')
      rx = int(info[0])
      ry = int(info[1])
      thickness = int(info[2]) / 100
      x_coordinate = (mx + rx) / 100
      y_coordinate = 10000 - ((my + ry) / 100)
      
      paf_line = '|RECORD=Pad|INDEXFORSAVE=0|SELECTION=FALSE|LAYER=MULTILAYER|LOCKED=FALSE|POLYGONOUTLINE=FALSE|USERROUTED=TRUE|UNIONINDEX=0|NAME=2|X=' + str(x_coordinate) + 'mil|Y=' + str(y_coordinate) + 'mil|XSIZE=' + str(thickness) + 'mil|YSIZE=' + str(thickness) + 'mil|SHAPE=ROUND|HOLESIZE=33.4646mil|ROTATION= 0.00000000000000E+0000|PLATED=TRUE|DAISYCHAIN=Load|CCSV=0|CPLV=0|CCWV=1|CENV=1|CAGV=1|CPEV=1|CSEV=1|CPCV=1|CPRV=1|CCW=10mil|CEN=4|CAG=10mil|CPE=0mil|CSE=4mil|CPC=20mil|CPR=20mil|PADMODE=0|SWAPID_PAD=|SWAPID_GATE=|&|0|SWAPPEDPADNAME=|GATEID=0|OVERRIDEWITHV6_6SHAPES=FALSE|DRILLTYPE=0|HOLETYPE=0|HOLEWIDTH=33.4646mil|HOLEROTATION= 0.00000000000000E+0000|PADXOFFSET0=0mil|PADYOFFSET0=0mil|PADXOFFSET1=0mil|PADYOFFSET1=0mil|PADXOFFSET2=0mil|PADYOFFSET2=0mil|PADXOFFSET3=0mil|PADYOFFSET3=0mil|PADXOFFSET4=0mil|PADYOFFSET4=0mil|PADXOFFSET5=0mil|PADYOFFSET5=0mil|PADXOFFSET6=0mil|PADYOFFSET6=0mil|PADXOFFSET7=0mil|PADYOFFSET7=0mil|PADXOFFSET8=0mil|PADYOFFSET8=0mil|PADXOFFSET9=0mil|PADYOFFSET9=0mil|PADXOFFSET10=0mil|PADYOFFSET10=0mil|PADXOFFSET11=0mil|PADYOFFSET11=0mil|PADXOFFSET12=0mil|PADYOFFSET12=0mil|PADXOFFSET13=0mil|PADYOFFSET13=0mil|PADXOFFSET14=0mil|PADYOFFSET14=0mil|PADXOFFSET15=0mil|PADYOFFSET15=0mil|PADXOFFSET16=0mil|PADYOFFSET16=0mil|PADXOFFSET17=0mil|PADYOFFSET17=0mil|PADXOFFSET18=0mil|PADYOFFSET18=0mil|PADXOFFSET19=0mil|PADYOFFSET19=0mil|PADXOFFSET20=0mil|PADYOFFSET20=0mil|PADXOFFSET21=0mil|PADYOFFSET21=0mil|PADXOFFSET22=0mil|PADYOFFSET22=0mil|PADXOFFSET23=0mil|PADYOFFSET23=0mil|PADXOFFSET24=0mil|PADYOFFSET24=0mil|PADXOFFSET25=0mil|PADYOFFSET25=0mil|PADXOFFSET26=0mil|PADYOFFSET26=0mil|PADXOFFSET27=0mil|PADYOFFSET27=0mil|PADXOFFSET28=0mil|PADYOFFSET28=0mil|PADXOFFSET29=0mil|PADYOFFSET29=0mil|PADXOFFSET30=0mil|PADYOFFSET30=0mil|PADXOFFSET31=0mil|PADYOFFSET31=0mil|PADJUMPERID=0\n'
      out_file.write(paf_line)
      print "Wrote PAD"

    elif line.find('ElementLine') is not -1:
      line = line[ line.find('[')+1 : line.find(']') ]
      info = line.split(' ')
      rx1 = int(info[0])
      ry1 = int(info[1])
      rx2 = int(info[2])
      ry2 = int(info[3])
      thickness = int(info[4]) / 100
      
      rx1_coordinate = (mx + rx1) / 100
      ry1_coordinate = 10000 - ((my + ry1) / 100)
      rx2_coordinate = (mx + rx2) / 100
      ry2_coordinate = 10000 - ((my + ry2) / 100)
      
      paf_line = '|RECORD=Track|INDEXFORSAVE=2|SELECTION=FALSE|LAYER=TOPOVERLAY|LOCKED=FALSE|POLYGONOUTLINE=FALSE|USERROUTED=TRUE|UNIONINDEX=0|X1=' + str(rx1_coordinate) + 'mil|Y1=' + str(ry1_coordinate) + 'mil|X2=' + str(rx2_coordinate) + 'mil|Y2=' + str(ry2_coordinate) + 'mil|WIDTH=' + str(thickness) + 'mil|SUBPOLYINDEX=0\n'
      out_file.write(paf_line)
      print "Wrote ElementLine"

  
# ---------------- Test area
for l in layers:
  if l.find('solder') is not -1:
    layer = 'BOTTOM'
  elif l.find('component') is not -1:
    layer = 'TOP'
  else:
    layer = None
  
  if layer is not None:
    for line in layers[l]:
      if line.find('Line') is not -1:
        line = line[ line.find('[')+1 : line.find(']') ]
        info = line.split(' ')
        x1 = int(info[0]) / 100
        y1 = 10000 - (int(info[1]) / 100)
        x2 = int(info[2]) / 100
        y2 = 10000 - (int(info[3]) / 100)
        thickness = int(info[4]) / 100
        
        paf_line = '|RECORD=Track|INDEXFORSAVE=2|SELECTION=FALSE|LAYER=' + layer + '|LOCKED=FALSE|POLYGONOUTLINE=FALSE|USERROUTED=TRUE|UNIONINDEX=0|X1=' + str(x1) + 'mil|Y1=' + str(y1) + 'mil|X2=' + str(x2) + 'mil|Y2=' + str(y2) + 'mil|WIDTH=' + str(thickness) + 'mil|SUBPOLYINDEX=0\n'
        out_file.write(paf_line)
        print "Wrote Bottom Line"
      
out_file.close()  
print "END"
