#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
sys.path.insert(0, "./leap") # load leap motion lib
import Leap
from rps_listener import RpsListener
from text2speech import text2speech

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
    time.sleep(0.7)

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
        time.sleep(5)
    # 最初はグーまでできた
    listener.stop_rock_check()

    msg = "じゃんけん"
    print_speech(msg)
    # predict
    rps_state = listener.start_rps_recognition()
    time.sleep(0.8)

    rps = rps_state.get_rps()

    msg = "ほい"
    print_speech(msg)
    time.sleep(1)

    print_speech(rps)
    # 停止
    listener.stop_measure()

def main():
    listener = RpsListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    # MVP
    rps_process(listener)

    controller.remove_listener(listener)

if __name__ == "__main__":
    main()
