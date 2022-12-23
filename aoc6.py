# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:02:57 2022

@author: Shaun
"""

#https://adventofcode.com/2022

#part 1 unique_len=4, part 2 unique_len=14
def day_6(unique_len):
    f = open('input_data/day_6.txt','r')
    feed = f.readlines()
    feed = feed[0]
    for i in range(len(feed)-unique_len):
        chunk = feed[i:i+unique_len]
        if sum([chunk.count(char) for char in chunk])==unique_len:
            print(str(i+unique_len))
            break
