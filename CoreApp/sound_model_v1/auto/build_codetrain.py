#!/usr/bin/python

filePrompts = open('prompts', 'r')
fileCodetrain = open('codetrain.scp', 'w')
for lineFile in filePrompts:
    fileName = lineFile.split(' ')[0].split('*/')[1]
    fileCodetrain.write("../train/wav/%s.wav ../train/mfcc/%s.mfc\n" % (fileName, fileName))
