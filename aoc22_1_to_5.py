# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:02:57 2022

@author: Shaun
"""

#https://adventofcode.com/2022

import pandas as pd

def day_1(part):
    cal_df = pd.read_excel('input_data/day_1_cals.xlsx')
    elf_count=0
    elf_cal=0
    elf_df = pd.DataFrame(columns=['elf_number','calories_carried'])
    for i in range(len(cal_df)):
        if pd.isna(cal_df.iloc[i,1]):
            temp_df = pd.DataFrame(columns=['elf_number','calories_carried'])
            temp_df.loc[0] = [elf_count, elf_cal]
            elf_df = elf_df.append(temp_df)
            elf_count=elf_count+1
            elf_cal=0
        else:
            elf_cal = elf_cal + cal_df.iloc[i,1]
    if part==1:
        print(str(get_max_value_rows(elf_df, number_of_vals=1).sum()[1]))
    elif part==2:
        print(str(get_max_value_rows(elf_df, number_of_vals=3).sum()[1]))

def get_max_value_rows(df, number_of_vals=1):
    temp_df = df.sort_values(by='calories_carried', ascending=False).copy()
    return temp_df.iloc[:number_of_vals]

def day_2():
    #Completed in Excel
    pass    

def day_3(part):
    data_df = pd.read_csv('input_data/day_3.txt', sep= ' ', names=['full_sack'])
    if part==1:
        df = data_df.copy()
        df['sack_1'] = df['full_sack'].apply(lambda text: text[:len(text) // 2])
        df['sack_2'] = df['full_sack'].apply(lambda text: text[len(text) // 2:])
        df['common_item'] = "N/A"
        df['priority'] = 0
        for index, [_, sack_1, sack_2, _, _] in df.iterrows():
            for i in sack_2:
                if i in sack_1:
                    df.loc[index, 'common_item'] = i
                    df.loc[index, 'priority'] = get_priority(i)
    elif part==2:
        df = data_df.iloc[::3, :].reset_index(drop=True).rename(columns={'full_sack':'first'})
        df['second'] = data_df.iloc[1::3, :].reset_index(drop=True)
        df['third'] = data_df.iloc[2::3, :].reset_index(drop=True)
        df['common_item'] = "N/A"
        df['priority'] = 0
        for index, [sack_1, sack_2, sack_3,_, _] in df.iterrows():
            for i in sack_1:
                if i in sack_2 and i in sack_3:
                    df.loc[index, 'common_item'] = i
                    df.loc[index, 'priority'] = get_priority(i)
    print(str(df.priority.sum()))

def get_priority(x):
    if x.islower():
        return ord(x)-96
    else:
        return ord(x)-64+26

def day_4(part):
    data_df = pd.read_csv('input_data/day_4.txt', sep= ',', names=['first', 'second'])
    df = data_df.copy()
    df[['first_left', 'first_right']] = df['first'].str.split('-', 1, expand=True)
    df[['second_left', 'second_right']] = df['second'].str.split('-', 1, expand=True)
    df[["first_left", "first_right", "second_left", "second_right"]] = df[["first_left", "first_right", "second_left", "second_right"]].apply(pd.to_numeric)
    if part==1:
        df['in_scope']=((df['first_left']>=df['second_left']) & (df['first_right']<=df['second_right']))\
            | ((df['second_left']>=df['first_left']) & (df['second_right']<=df['first_right']))
    elif part==2:
        df['in_scope']=((df['first_right']>=df['second_left']) & (df['first_right']<=df['second_right']))\
        | ((df['first_left']>=df['second_right']) & (df['first_left']<=df['second_left']))\
            | ((df['second_right']>=df['first_left']) & (df['second_right']<=df['first_right']))\
                | ((df['second_left']>=df['first_right']) & (df['second_left']<=df['first_left']))
    print(str(len(df[df['in_scope']==True])))
    
def day_5(part):
    instructions_df = pd.read_csv('input_data/day_5_instructions.txt', names=['instructions'])
    instructions = instructions_df['instructions'].to_list()
    
    crates =  pd.read_excel('input_data/day5_crates_starting.xlsx')
    crate_lists = [crates[i+1].dropna().tolist() for i in range(len(crates.columns))]
    
    if part==1:
        for instruction in instructions:
            amount, start, end = pull_action(instruction)
            for i in range(amount):
                crate_lists[end].append(crate_lists[start][-1])
                crate_lists[start] = crate_lists[start][:-1]
    elif part==2:
        for instruction in instructions:
            amount, start, end = pull_action(instruction)
            crate_lists[end].extend(crate_lists[start][-amount:])
            crate_lists[start] = crate_lists[start][:-amount]
            
    print(''.join([crate_list[-1][1] for crate_list in crate_lists]))

def pull_action(instruction):
    action = instruction[5:]
    amount, rest = action.split(' from ')
    start, end = rest.split(' to ')
    return int(amount), int(start)-1, int(end)-1
