#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

class RockState():
    """
    Store hand data and return whether it's rock or not
    """
    finger_names = ['thumb', 'index', 'middle', 'ring', 'pinky']
    finger_hand_angle = 95
    rock_count = 0
    # number of frame
    rock_count_thres = 10
    non_rock_count = 0
    # number of frame
    non_rock_count_thres = 3

    def __init__(self):
        pass

    def update_hand_data(self, hand):
        hand_data = [None] * 5
        hand_direction = hand.direction

        for fng in hand.fingers:
            angle_hand_fng = hand_direction.angle_to(fng.direction) * 180 / math.pi
            hand_data[fng.type] = angle_hand_fng
        # check angle without thumb data
        if all([angle > self.finger_hand_angle for angle in hand_data[1:]]):
            # count as rock
            self.rock_count += 1
        else:
            self.non_rock_count +=1
            if self.non_rock_count >= self.non_rock_count_thres:
                # reset if the angle of finger-hand is narrow continuously
                self.rock_count = 0
                self.non_rock_count = 0

    def is_rock_state(self):
        if self.rock_count >= self.rock_count_thres:
            return True
        else:
            return False
