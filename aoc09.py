# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:02:57 2022

@author: Shaun
"""

#https://adventofcode.com/2022

import pandas as pd
    
def day_9(part):
    data_df = pd.read_csv('input_data/day_9.txt', names=['runs'])
    moves = list(data_df['runs'])
    head= [0,0]
    #tail = [0,0]
    
    for move in moves:
        direction, amount = move.split(' ')
        amount=int(amount)
        if direction=='R':
            head = [head[0]+amount, head[1]]
        elif direction=='L':
            head = [head[0]-amount, head[1]]
        elif direction=='U':
            head = [head[0], head[1]-amount]
        elif direction=='L':
            head = [head[0], head[1]+amount]

def distance(head, tail):
    return max(head[0]-tail[0], head[1]-tail[1])
