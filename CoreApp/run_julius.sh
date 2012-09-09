#!/bin/bash

julius -quiet -input mic -C julius.jconf | grep sentence1 2> /dev/null  