#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, "./leap") # load leap motion lib
import os
from datetime import datetime
import pickle
import math
from rock_state import RockState
from rps_state import RpsState

import Leap
from Leap import Vector

class RpsListener(Leap.Listener):
    finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    xyz = ["x", "y", "z"]
    origin = Vector(0,0,0)
    is_measuring = False
    rock_state = None
    rps_state = None

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def get_hand_data(self, hand):
        # heuristic way
        hand_data = [None] * 7
        hand_data[0] = hand.id
        hand_data[1] = hand.confidence
        idx = 2
        hand_direction = hand.direction
        palm_normal = hand.palm_normal
        for fng in hand.fingers:
            angle_hand_fng = hand_direction.angle_to(fng.direction) * 180 / math.pi
            angle_norm_fng = palm_normal.angle_to(fng.direction) * 180 / math.pi
            if angle_norm_fng > 90:
                angle_hand_fng = angle_hand_fng * -1
            hand_data[idx + fng.type] = angle_hand_fng
        return hand_data

    def start_measure(self):
        self.is_measuring = True

    def start_rock_check(self):
        self.rock_state = RockState()
        return self.rock_state

    def stop_rock_check(self):
        self.rock_state = None

    def start_rps_recognition(self):
        self.rps_state = RpsState()
        return self.rps_state

    def stop_rps_recognition(self):
        self.rps_state = None

    def stop_measure(self):
        """
        Reset all state info
        """
        self.is_measuring = False
        self.stop_rock_check()
        self.stop_rps_recognition()

    def on_frame(self, controller):
        if self.is_measuring == False:
            return
        frame = controller.frame()
        if len(frame.hands) == 0:
            print("No data in this frame")
            return
        # use first hand
        hand = frame.hands[0]
        # they do not contain valid tracking data and do not correspond to a physical entity
        if hand.is_valid == False:
            print("Not valid hand")
            return
        # store hand data to rock state
        if self.rock_state != None:
            self.rock_state.update_hand_data(hand)
        if self.rps_state != None:
            self.rps_state.update_hand_data(hand)
