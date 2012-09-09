#!/bin/bash

rm -f tts.mp3
wget -O tts.mp3 -U "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2" "http://translate.google.com/translate_tts?tl=ru&q=$1"
mpg123 tts.mp3
rm -f tts.mp3