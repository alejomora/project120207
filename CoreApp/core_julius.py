#!/usr/bin/python
# -*- coding: utf-8 -*-

import pexpect
import re

def process_julius(out_text, logHand, manDic, manEvt):
    match_res = re.match(r'(.*)sentence1(\.*)', out_text, re.S)
    if match_res:
        get_confidence(out_text, logHand, manDic, manEvt)
    else:
        pass

def get_confidence(out_text, logHand, manDic, manEvt):
    linearray = out_text.split("\n")
    for line in linearray:
        if line.find('sentence1') != -1:
            sentence1 = line
        elif line.find('cmscore1') != -1:
            cmscore1 = line
        elif line.find('score1') != -1:
            score1 = line
    cmscore_array = cmscore1.split()
    #process sentence
    err_flag = False
    for score in cmscore_array:
        try:
            ns = float(score)
        except ValueError:
            continue
        if (ns < 0.999):
            err_flag = True
            logHand.debug("confidence error: %s %s" % (ns, sentence1))
    score1_val = float(score1.split()[1])
    if score1_val < -35000:
        err_flag = True
        logHand.debug("score1 error: %s %s" % (score1_val, sentence1))
    if (not err_flag):
        manDic['julius'] = sentence1.strip().split('IDENT')[1].split('</s>')[0].strip()
        logHand.debug("sentence1: %s" % (sentence1))
        logHand.debug("score1: %s" % (score1))
        manEvt.set()
        #process sentence
        #process_sentence(sentence1)
    else:
        pass

def main(logHand, manDic, manEvt):

    child = pexpect.spawn ('julius -input mic -C julius.jconf')
 
    while True:
        try:
            i = child.expect('please speak', timeout = None)
            process_julius(child.before, logHand, manDic, manEvt)
        except KeyboardInterrupt:
            logHand.debug("Exit julius module.")
            child.close(force=True)
            break

if __name__ == "__main__":
    print " --------------------------------- "
    print "| Module core julius. Version 1.2 |"
    print " --------------------------------- "
