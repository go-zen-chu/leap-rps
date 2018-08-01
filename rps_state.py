#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from collections import deque

class RpsState():
    """
    recognizing rock paper or scissors
    """
    rps_arr = ["rock", "paper", "scissors"]
    rps_queue_len = 8 # save past 8 frame in queue
    rps_queue = deque(["rock"] * 8, 8) # default is rock
    rock_finger_hand_angle = 85 # higher than this
    paper_finger_hand_angle = 60 # lower than this
    scissors_finger_hand_angle = 60 # lower than this
    rps_recognize_thres = 10 # frame
    rps_map = {"rock": 0, "paper": 0, "scissors": 0}
    logger = None

    def __init__(self, logger):
        self.logger = logger

    def update_hand_data(self, hand):
        # 0: index, 1: middle, 2: ring, 3: pinky
        hand_data = [None] * 4
        hand_direction = hand.direction
        palm_normal = hand.palm_normal
        for fng in hand.fingers:
            # check angle without thumb data
            if fng.type == 0:
                continue
            angle_hand_fng = hand_direction.angle_to(fng.direction) * 180 / math.pi
            angle_norm_fng = palm_normal.angle_to(fng.direction) * 180 / math.pi
            if angle_norm_fng > 90:
                angle_hand_fng = angle_hand_fng * -1
            hand_data[fng.type - 1] = angle_hand_fng
        # self.logger.info(hand_data)

        # if all of
        if all([angle > self.rock_finger_hand_angle for angle in hand_data]):
            # count as rock
            self.rps_queue.append(self.rps_arr[0])
        elif all([angle < self.paper_finger_hand_angle for angle in hand_data]):
            # count as paper
            self.rps_queue.append(self.rps_arr[1])
        # it's important to recognize scissors after rock, paper
        # because rock, paper are easy to detect
        elif hand_data[0] < self.scissors_finger_hand_angle and hand_data[1] < self.scissors_finger_hand_angle:
            # if index and middle finger is open, count as scissors
            self.rps_queue.append(self.rps_arr[2])

    def get_rps(self):
        # according to our preliminary investigation, rps is performed during 90ms (around 5-10frame)
        # initialize
        for rps in self.rps_arr:
            self.rps_map[rps] = 0
        # count inside queue
        for rps in self.rps_queue:
            self.rps_map[rps] += 1
        # prediction through vote (getting max value key in rps_map)
        rps_predict = max([(v,k) for k,v in self.rps_map.items()])[1]
        return rps_predict
