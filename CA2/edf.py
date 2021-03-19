# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 18:31:26 2021

@author: eleojjz
"""
import math
from operator import attrgetter

class Task:
    def __init__(self, details, idx):
        self.completed = False
        self.progress = 0
        self.job_start = -1
        self.job_completed = 0
        self.next_allowed_task = 0
        self.ready = True
        
        split = details.split(',')
        self.tid = idx
        self.wcet = int(split[0])
        self.next_deadline = int(split[1])
        self.period = int(split[2])
    
    def print_details(self):
        print('Task ID: ' + str(self.tid) + ' WCET: ' + str(self.wcet) + 
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
    
def get_earliest_deadline_task_list():
    return sorted(task_set, key = attrgetter('next_deadline'))

class Scheduler:
    def __init__(self):
        self.curr_tid = -1;
        self.is_busy = False;
        
    def get_task_from_id(self, tid):
        for task in task_set:
            if task.tid == tid:
                return task
        return None
    
    def update_tasks(self, t):
        #check which task has the earliest deadline
        task_list = get_earliest_deadline_task_list()
        
       # deadlines = []
       # for task in task_list:
       #    deadlines.append(task.next_deadline)
       # print('{} {} {}'.format(deadlines[0], deadlines[1], deadlines[2]))
        
        #list of tasks ordered based on their earliest deadlines
        for task in task_list:
            if not task.completed:
                if not self.is_busy:
                    if t >= task.next_allowed_task:
                        if task.job_start == -1:
                            task.job_start = t
                            self.curr_tid = task.tid
                            self.is_busy = True;
                            print('Task {} has started at T={}'.format(task.tid, t))
                    
                if task.progress >= task.wcet:
                    task.completed = True
                    self.curr_tid = -1
                    self.is_busy = False;
                    print('Task {} completed execution from T={} to T={}'.format(task.tid, task.job_start, t))
                    
                if self.curr_tid == task.tid:
                    task.progress += 1
                
            if (task.next_deadline == t):
                task.completed = False
                task.progress = 0
                task.job_start = -1
                task.next_deadline += task.period
                task.next_allowed_task += task.period
                print('Task {} has reached its deadline of T={}. The new deadline is T={}'.format(task.tid, (task.next_deadline-task.period), task.next_deadline))
  
    
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
scheduler.run(hyper_period)

