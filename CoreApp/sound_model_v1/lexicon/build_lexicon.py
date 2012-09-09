#!/usr/bin/python

import sys

filePrompts	= open('words', 'r')
fileDict	= open('msu_ru_nsh.dic', 'r')
fileLexicon	= open('voxforge_lexicon', 'w')
prompts = []
for lineFile in filePrompts:
    prompt = lineFile.split(' ')[0]
    prompts.append(prompt.strip())

for item in prompts:
    print item

dictWords = {'SENT-END':"SENT-END [] sil\n", 'SENT-START':"SENT-START [] sil\n"}
ic = 0 
for lineFile in fileDict:
    ic=ic+1
    words  = lineFile.split(' ')[0]
    lexic  = lineFile[len(words):]
    if words in prompts:
	dictWords[words] = "%s [%s] %s" % (words, words, lexic)
	#fileLexicon.write("%s [%s] %s" % (words, words, lexic))
	print "%s " % ic
	

for key in sorted(dictWords.iterkeys()):
    fileLexicon.write(dictWords[key])
