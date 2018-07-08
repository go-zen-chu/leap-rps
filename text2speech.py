#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands
import platform

def text2speech(msg):
    system = platform.system()
    if system == "Darwin":
        # please set your speech config in mac according to your language
        commands.getoutput("say '{}'".format(msg))
    else:
        raise NotImplementedError("Only supported in macOS, yet")
