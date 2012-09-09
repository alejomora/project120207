#!/usr/bin/python
# -*- coding: utf-8 -*-

import multiprocessing, logging, time

import core_julius
import core_speech

def coreJulius(logHand, manDic, manEvt):
    logHand.info('Start modeule julius')
    core_julius.main(logHand, manDic, manEvt)


def coreSpeech(logHand, manDic, manEvt):
    logHand.info('Start modeule speech')
    core_speech.main(logHand, manDic, manEvt)


def main():
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.DEBUG)

    logger.info('Start main module')

    managerSpeech = multiprocessing.Manager()
    managerSpeechDict = managerSpeech.dict()
    managerSpeechEvent = managerSpeech.Event()

    juliusProc = multiprocessing.Process(target=coreJulius, args=(logger, managerSpeechDict, managerSpeechEvent))
    juliusProc.name = "CoreJulius"
    juliusProc.daemon = True
    juliusProc.start()

    speechProc = multiprocessing.Process(target=coreSpeech, args=(logger, managerSpeechDict, managerSpeechEvent))
    speechProc.name = "CoreSpeech"
    speechProc.daemon = True
    speechProc.start()

    core_speech.play_sound("do_start.wav", logger)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            juliusProc.join(2)
            if juliusProc.is_alive():
                juliusProc.terminate()
            speechProc.join(2)
            if speechProc.is_alive():
                speechProc.terminate()
            managerSpeech.shutdown()
            break


if __name__ == "__main__":
    print " -------------------------- "
    print "| Main module clock system |"
    print " -------------------------- "

    #Run system

    main()
