#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import socket
import subprocess
import core_tools

def check_festival():

    host = '127.0.0.1'
    port = 1314

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.shutdown(2)
        return True
    except:
        return False

def say_prompt(prompt, logHand):    
    global sayProc
    play_sound("do_work.wav", logHand)        
    logHand.debug("Festival: %s" % prompt)
    sayProc = subprocess.Popen("echo \"%s\" | festival_client --async --ttw --aucommand ' mplayer -really-quiet $FILE'" % prompt, shell=True)

def say_prompt_google(prompt, logHand):
    global sayProc
    logHand.debug("Google TTS: %s" % prompt)
    sayProc = subprocess.Popen("./google_tts.sh \"%s\"" % prompt, shell=True)

def play_sound(sound, logHand):
    global sayProc
    logHand.debug("Play sound: %s" % sound)
    sayProc = subprocess.Popen(" mplayer -really-quiet ./sounds/'%s'" % sound, shell=True)

def work_say(command, logHand):
    
    global sayProcGlob
    global isSleepGlob

    logHand.debug("Command: %s" % command)
    logHand.debug("Is sleep: %s" % isSleepGlob)
    logHand.debug("Proc is None: %s" % sayProcGlob is None)    

    if command.upper() == "STOP" and not isSleepGlob:
        if sayProcGlob is not None:
            if sayProcGlob.poll() is None:
                sayProcGlob.kill()
	
    elif command.upper() == "SLEEP":
        if sayProcGlob is not None:
            if sayProcGlob.poll() is None:
                sayProcGlob.kill()
        if not isSleepGlob:
            play_sound("do_sleep.wav", logHand)
            isSleepGlob = True
	
    elif command.upper() == "UP":
        if sayProcGlob is not None:
            if sayProcGlob.poll() is None:
                sayProcGlob.kill()
        if isSleepGlob:    
            play_sound("do_up.wav", logHand)
            isSleepGlob = False	
	
    elif not isSleepGlob: 
        if sayProcGlob is not None:
            if sayProcGlob.poll() is not None:
                work_over_say(command, logHand)
        else:
            work_over_say(command, logHand)
    

def work_over_say(command, logHand):
    
    logHand.debug("Over say command: %s" % command)
    
    if command.upper() == "ADRESS":
        #play_sound("do_foo.wav", logHand)
	    say_prompt_google(core_tools.getIfIPToSay(), logHand)
    elif command.upper() == "TIME":
        #play_sound("do_foo.wav", logHand)
	    say_prompt(core_tools.getTimeToSay(), logHand)
    elif command.upper() == "DATE":
        #play_sound("do_foo.wav", logHand)
	    say_prompt_google(core_tools.getDateToSay(), logHand)
    elif command.upper() == "NEWS":
        play_sound("do_foo.wav", logHand)
    elif command.upper() == "MAIL":
        play_sound("do_foo.wav", logHand)
    elif command.upper() == "STATUS":
        play_sound("do_foo.wav", logHand)
    elif command.upper() == "EVENTS OF TOMORROW":
        play_sound("do_foo.wav", logHand)
    elif command.upper() == "EVENTS OF TODAY":
        play_sound("do_foo.wav", logHand)
    elif command.upper() == "EVENTS TODAY":
        play_sound("do_foo.wav", logHand)
    elif command.upper() == "WEATHER OF TOMORROW":
        play_sound("do_foo.wav", logHand)
    elif command.upper() == "WEATHER OF TODAY":
        play_sound("do_foo.wav", logHand)
    elif command.upper() == "WEATHER TODAY":
        play_sound("do_foo.wav", logHand)

def main(logHand, manDic, manEvt):
    
    global sayProcGlob
    global isSleepGlob    
    
    sayProcGlob = None
    isSleepGlob = False

    while True:
        try:
            logHand.debug("Wait event to speech.")
            manEvt.wait()
            if 'julius' in manDic:
                work_say(manDic['julius'], logHand)
            manEvt.clear()
        except KeyboardInterrupt:
            logHand.debug("Exit speech module.")
            break

###########################################################################################################

if __name__ == "__main__":
    print " --------------------------------- "
    print "| Module core speech. Version 1.1 |"
    print " --------------------------------- "
