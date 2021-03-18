# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 18:31:26 2021

@author: eleojjz
"""
import math
from operator import attrgetter

class Task:
    def __init__(self, details, idx):
        self.offset = 0;
        self.completed = False;
        
        split = details.split(',')
        self.task_id = idx
        self.exec_time = int(split[0])
        self.next_deadline = int(split[1])+offset
        self.period = int(split[2])
    
    def print_details(self):
        print('Task ID: ' + str(self.task_id) + ' Exec Time: ' + str(self.exec_time) + 
              ' Deadline: ' + str(self.deadline) + 
              ' Period: ' + str(self.period))


def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def utilization_test(task_set):
    util = 0;
    for task in task_set:
        util += float(task.exec_time/task.period)
    print('Schedulability test: U = ' + str(util))
    if (util <= 1):
        return True
    else:
        return False
        
    
# Reading task set
task_set = []
f = open('taskset.txt', 'r')
num_tasks = f.readline()
hyper_period = 1;
for i in range(int(num_tasks)):
    task = Task(f.readline().strip(), i+1)
    task.print_details()
    hyper_period = lcm(task.period, hyper_period)
    task_set.append(task)

print('Hyper period of task set is ' + str(hyper_period) + ' T.')
utilization_test(task_set)
   
#start scheduling
scheduler = Scheduler(task_set)

