# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 18:31:26 2021

@author: eleojjz
"""
import math
from operator import attrgetter

class Task:
    def __init__(self, details, idx):
        self.completed = False;
        self.progress = 0;
        self.job_start = 0;
        
        split = details.split(',')
        self.task_id = idx
        self.wcet = int(split[0])
        self.next_deadline = int(split[1])
        self.period = int(split[2])
    
    def print_details(self):
        print('Task ID: ' + str(self.task_id) + ' WCET: ' + str(self.wcet) + 
              ' Deadline: ' + str(self.next_deadline) + 
              ' Period: ' + str(self.period))

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def utilization_test(task_set):
    util = 0;
    for task in task_set:
        util += float(task.wcet/task.period)
    print('Schedulability test: U = ' + str(util))
    if (util <= 1):
        return True
    else:
        return False
    
def get_earliest_deadline_task():
    return min(task_set, key = attrgetter('next_deadline'))

class Scheduler:
    def __init__(self):
        self.running_tasks = set()
        self.curr_task = -1
        
    def update_task(self, t):
        # updating all currently running tasks
        for task in self.running_tasks:
        
        
        
    def run(self, duration):
        t = 0;
        while t < duration:
            self.update_tasks(t)
            t += 1
        print('Simulation Complete.')
        
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
scheduler = Scheduler()
scheduler.run(hyper_period*3)

