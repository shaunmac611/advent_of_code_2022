# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 11:35:21 2022

@author: Shaun
"""

import pandas as pd
import math

def day_10():
    #part 1
    df = pd.read_csv('input_data/day_10.txt', sep=' ', names=['action','count'])
    for i in range(240 - len(df)):
        df = df.append(pd.Series(['Tail',0],index=['action','count']), ignore_index=True)
    df['X'] = 1
    df['cycle'] = df.index + 1

    run_cycle=0
    for i in range(len(df)):
        if df.iloc[i,0]=='noop':
            run_cycle = run_cycle+1
        if df.iloc[i,0]=='addx':
            run_cycle = run_cycle+2
            df.loc[run_cycle:, 'X'] = df.loc[run_cycle, 'X'] + df.iloc[i,1]
            
    df['signal_strength'] = df['X']*df['cycle']
    
    answer=0
    for check in [20,60,100,140,180,220]:
        answer = answer+df.loc[df['cycle']==check, 'signal_strength'].iloc[0]
    print(str(answer))
        
    screen = pd.DataFrame('.', index=[x for x in range(6)], columns=[y for y in range(40)])
    for cycle in range(1,240+1):
        sprite = pd.DataFrame(False, index=[x for x in range(6)], columns=[y for y in range(40)])
        horizontal_spirte=df.loc[df.cycle==cycle,'X'].iloc[0]
        horizontal_draw, vertical_draw = get_coordinates(cycle-1)
        for width in [-1,0,1]:
            horizontal_spirte_full = horizontal_spirte+width
            if horizontal_spirte_full >=0 and horizontal_spirte_full<=39:
                sprite.loc[(vertical_draw),(horizontal_spirte_full)] = True

        if sprite.loc[(vertical_draw),(horizontal_draw)]:
            screen.loc[(vertical_draw),(horizontal_draw)]='#'
    screen.to_csv('output_data/day_10_output.csv')

def get_coordinates(val):
    horizontal = round(val%40)
    vertical = round(math.floor(val/40))        
    return horizontal, vertical