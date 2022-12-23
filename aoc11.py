# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 13:29:08 2022

@author: Shaun
"""

import pandas as pd
import math

def day_11(rounds=10000, div_3=False):
    monkey_list, lcm_div = read_input_data(div_3=div_3)
    lcm_final = 1
    for num in lcm_div:
        lcm_final = lcm(lcm_final,num)
    for i in range(rounds):
        for i in range(len(monkey_list)):
            monkey_list[i].inspections()
            thrown_items = monkey_list[i].throw_items()
            for monkey, item in thrown_items:
                if item>lcm_final:
                    monkey_list[monkey].catch(item%lcm_final)
                else:
                    monkey_list[monkey].catch(item)
    final_answer = get_answer(monkey_list)
    print(str(final_answer))

class Monkey:
    def __init__(self, description, div_3=True):
        self.div_3=div_3
        self.description = description
        self.number=self.number()
        self.item_list=self.starting_items()
        self.operation, self.operation_full=self.init_operation()
        self.full_test, self.test, self.test_true, self.test_false =self.init_test()
        self.thrown_items=[]
        self.inspection_count = 0
        
    def number(self):
        return int(self.description[0].split('Monkey ')[1][:-1])
    
    def starting_items(self):
        item_list = self.description[1].split('Starting items: ')[1].split(', ')
        return [int(i) for i in item_list]
    
    def init_operation(self):
        operation_full = self.description[2].split('Operation: ')[1]
        operation = operation_full.split('new = old ')[1]
        return operation, operation_full
    
    def init_test(self):
        full_test = self.description[3].split('Test: ')[1]
        test = int(full_test.split(' by ')[1])
        test_true = int(self.description[4].split('If true: throw to monkey ')[1])
        test_false = int(self.description[5].split('If false: throw to monkey ')[1])
        return full_test, test, test_true, test_false
    
    def to_df(self):
        d = {'number':[self.number],
             'starting_items':[self.starting_items],
             'operation':[self.operation],
             'test':[self.test],
             'true':[self.test_true],
             'false':[self.test_false],
             }
        return pd.DataFrame(d)
    
    def to_string(self):
        return 'Monkey ' + self.number + ' has ' + self.starting_items
    
    def inspections(self):
        for item in self.item_list:
            item = self.inspect(item)
            if item%self.test==0:
                self.throw(self.test_true, item)
            else:
                self.throw(self.test_false, item)
        self.item_list=[]
    
    def inspect(self, item):
        action = self.operation[0]
        if str(self.operation[1:]) == ' old':
            value = item
        else:
            value = int(self.operation[1:])
        if action=='+':
            item = item+value
        elif action=='-':
            item = item-value
        elif action=='*':
            item = item*value
        elif action=='/':
            item = item/value
        else:
            print('action not found')
        if self.div_3:
            item = math.floor(item/3)
        self.inspection_count = self.inspection_count + 1
        return item
    
    def throw(self, monkey_number, item):
        self.thrown_items.append([monkey_number, item])
    
    def catch(self, item):
        self.item_list.append(item)
    
    def throw_items(self):
        temp_throw_items = self.thrown_items 
        self.thrown_items = []
        return temp_throw_items
    
def read_input_data(div_3=True):
    monkey_file = open('input_data/day_11.txt', 'r')
    Lines = monkey_file.readlines()
    monkey_list=[]
    description=[]
    for line in Lines:
        if line=='\n':
            monkey_list.append(Monkey(description, div_3))
            description = []
        else:
            description.append(line.strip())
    lcm_div=[]
    for monk in monkey_list:
        lcm_div.append(monk.test)
    return monkey_list, lcm_div

def get_answer(monkey_list):
    answers = []
    for i in range(len(monkey_list)):
        answers.append(monkey_list[i].inspection_count)
    print(answers)
    final_answer = max(answers)
    answers.remove(max(answers))
    final_answer = final_answer * max(answers)
    return final_answer

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)