# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:02:57 2022

@author: Shaun
"""

#https://adventofcode.com/2022

import pandas as pd

def day_8(part):
    data_df = pd.read_csv('input_data/day_8.txt', names=['runs'])
    df=data_df.copy()
    for i in range(len(df.iloc[1,0])):
        df[str(i)]= df['runs'].astype(str).str[i]
    df = df.drop(columns=['runs'])
    df = df.apply(pd.to_numeric)
    
    visible_df = df.copy()
    scenic_df = df.copy()
    
    if part==1:
        for i in range(len(df)):
            for j in range(len(df.columns)):
                visible_df.iloc[i,j] = check_visible(df,i,j)
        print(str(count_vals(visible_df, True)))
    elif part==2:
        for i in range(len(df)):
            for j in range(len(df.columns)):
                scenic_df.iloc[i,j] = check_scenic(df,i,j)
        print(str(scenic_df.max().max()))
                       
def check_visible(df,i,j):
    if i==0 or j==0 or i==len(df)-1 or j==len(df.columns)-1:
        return True
    else:
        tree_line = min(df.iloc[:i,j].max(),
                        df.iloc[i+1:,j].max(),
                        df.iloc[i,:j].max(),
                        df.iloc[i,j+1:].max())
        if df.iloc[i,j]>tree_line:
            return True
        else:
            return False

def check_scenic(df,i,j):
    left = check_direction(df,i,j,'left')
    right = check_direction(df,i,j,'right')
    up = check_direction(df,i,j,'up')
    down = check_direction(df,i,j,'down')
    return left*right*up*down

    
def check_direction(df,i,j,direction):
    tree_height=df.iloc[i,j]
    scenery=0
    
    if direction in ['left','right']:
        if direction=='left':
            range_loop = range(j-1, -1, -1)
        elif direction=='right':
            range_loop = range(j+1, len(df.columns), 1)
        for x in range_loop:
            tree = df.iloc[i, x]
            if tree < tree_height:
                scenery = scenery+1
            elif tree == tree_height:
                scenery = scenery+1
                break
            else:
                break
        
    elif direction in ['up','down']:
        if direction=='up':
            range_loop = range(i-1, -1, -1)
        elif direction=='down':
            range_loop = range(i+1, len(df), 1)
        for x in range_loop:
            tree = df.iloc[x, j]
            if tree < tree_height:
                scenery = scenery+1
            elif tree == tree_height:
                scenery = scenery+1
                break
            else:
                break
    return scenery

def count_vals(df, val):
    count=0
    for i in range(len(df.columns)):
        count = count + df.iloc[i].value_counts()[True]
    return count
