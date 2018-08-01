#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
sys.path.insert(0, "./leap") # load leap motion lib
import Leap
from rps_listener import RpsListener
from text2speech import text2speech
from logging import getLogger, DEBUG, StreamHandler

rps_file_name = 'rps.txt'

def print_speech(msg):
    text2speech(msg)
    print(msg)

def rps_prepare(listener):
    """
    Before rps. We need to confirm that leap recognizing paper & rock.
    Otherwise, we will get bad recognition.
    """
    msg = "手を開いてください"
    print_speech(msg)
    time.sleep(3)

    msg = "最初は"
    print_speech(msg)
    time.sleep(0.5)

    msg = "グー"
    print_speech(msg)
    # 測定
    listener.start_measure()
    rock_state = listener.start_rock_check()
    time.sleep(1)
    # グーを認識できているか？
    return rock_state.is_rock_state()

def rps_process(listener):
    while rps_prepare(listener) == False:
        # could not recognize rock state. try again
        msg = "正しく認識できませんでした。もう一度おねがいします"
        print_speech(msg)
        time.sleep(3)
    # 最初はグーまでできた
    listener.stop_rock_check()
    # start prediction
    rps_state = listener.start_rps_recognition()

    msg = "じゃんけん"
    print_speech(msg)
    time.sleep(0.7)

    msg = "ほい"
    print_speech(msg)
    rps = rps_state.get_rps()
    print(rps_state.rps_queue)
    print(rps)
    # write result to file
    with open(rps_file_name,'w') as f:
        f.write(rps)
    # print_speech(rps)

    time.sleep(1)
    # rps
    if os.path.exists(rps_file_name):
        os.remove(rps_file_name)
    # 停止
    listener.stop_measure()

def main():
    # setup logger
    logger = getLogger(__name__)
    logger.setLevel(DEBUG)
    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)
    logger.addHandler(stream_handler)
    logger.propagate = False

    # setup leap listener
    listener = RpsListener()
    listener.set_logger(logger)
    controller = Leap.Controller()
    controller.add_listener(listener)
    # MVP
    rps_process(listener)

    controller.remove_listener(listener)

if __name__ == "__main__":
    main()
