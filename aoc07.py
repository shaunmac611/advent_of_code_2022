# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:02:57 2022

@author: Shaun
"""

#https://adventofcode.com/2022

import pandas as pd

def day_7(part):
    data_df = pd.read_csv('input_data/day_7.txt', names=['runs'])
    
    df=data_df.copy()
    df.loc[df['runs'].str.contains('dir'),'dirs'] = df['runs'].astype(str).str[4:]
    df.loc[df['runs'].astype(str).str[0]=='$','commands'] = df['runs']
    df.loc[df['runs'].str.contains('cd'), 'parent_dir'] = df['commands'].astype(str).str[4:]
    df['parent_dir'].fillna(method='ffill', inplace=True)
    df['dirs'] = df['parent_dir'] + '/' + df['dirs']
    df.loc[df['dirs'].str.contains('//').fillna(False),'dirs'] = df['dirs'].astype(str).str[2:]
    
    for i in range(len(df)):
        if df.iloc[i,0][:6] == '$ cd /':
            df.iloc[i,1] = '/'
        if df.iloc[i,0][:4] == '$ cd' and df.iloc[i,0][:7] != '$ cd ..'and i>0:
            dir_name = df.iloc[:i,1][df.iloc[:i,0].str.contains(df.iloc[i,0][5:])]
            df.iloc[i,1] = dir_name.iloc[0]
    
    
    dir_df=pd.DataFrame()
    for i in range(len(df)):
        if df.iloc[i,0] == '$ ls':
            count=1
            while i+count<len(df) and pd.isna(df.iloc[i+count,2]):
                if df.iloc[i+count,0][0] != "$":
                    if df.iloc[i+count,0][:3] == 'dir':
                        dir_df.loc[count-1, df.iloc[i-1,1][5:]] = df.iloc[i+count,1]
                    else:
                        dir_df.loc[count-1, df.iloc[i-1,0][5:]] = df.iloc[i+count,0]
                count=count+1
    
    dir_size_df=pd.DataFrame()
    count=0
    for dir_name in dir_df.columns:
        dir_size_df.loc[count,'name'] = dir_name
        dir_name_lookup, count_from_before = dir_name.split('_')
        dir_size_df.loc[count,'size'] = calculate_dir_size(dir_df, dir_name_lookup, total_size=0)
        count=count+1
    dir_size_df[dir_size_df['size']<=100000]['size'].sum()
    
def calculate_dir_size(dir_df, dir_name, total_size=0):
    for item in dir_df[dir_name]:
        if not pd.isna(item):
            if item[:3]=='dir':
                total_size = calculate_dir_size(dir_df, item[4:], total_size)
            else:
                size, file_name = item.split(' ')
                total_size = total_size+int(size)
    return total_size
