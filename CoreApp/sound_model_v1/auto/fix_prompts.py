#!/usr/bin/python

import sys

filePromptsBad	= open('promptsbad', 'r')
filePrompts	= open('prompts', 'w')
for lineFile in filePromptsBad:
    num		= lineFile.split('.')[0]
    prompt	= lineFile.split('.')[1]
    filePrompts.write("*/sample%s %s" % (num, prompt))
