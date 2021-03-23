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
        self.num_jobs_completed = 0
        self.num_jobs_missed = 0
        self.next_allowed_task = 0
        self.ready = True
        self.num_preemptions = 0
        
        split = details.split(',')
        self.tid = idx
        self.wcet = int(split[0])
        self.next_deadline = int(split[1])
        self.period = int(split[1])
    
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
    
def get_earliest_deadline_task_list(task_list):
    return sorted(task_list, key = attrgetter('next_deadline'))


class Scheduler:
    def __init__(self):
        self.curr_tid = -1
        self.tasks_completed = 0
        self.tasks_missed = 0
        
    def get_task_from_id(self, tid):
        for task in task_set:
            if task.tid == tid:
                return task
        return None

    def schedule(self, t):
        for task in task_set:
            if task.tid == self.curr_tid:
                task.progress += 1
                if task.progress == task.wcet:
                    task.completed = True
            
            if task.next_deadline == t:
                if not task.completed:
                    print('Deadline for task {} is missed at T='.format(task.tid, t))
                task.next_deadline += task.period
                task.progress = 0
                task.completed = False
        
        task_list = get_earliest_deadline_task_list(task_set)
        
        if self.curr_tid == task_list[0].tid:
            print('Task {} ran from T={} to T={}'.format(task.tid, task.job_start, )
        
    
    def run(self, duration):
        t = 0;
        while t < duration:
            self.schedule(t)
            t += 1
        print('Simulation Complete.')
        print('Tasks completed: {}.'.format(self.tasks_completed))
        print('Tasks missed: {}'.format(self.tasks_missed))
        
# Reading task set
task_set = []
f = open('taskset.txt', 'r')
num_tasks = f.readline()
hyper_period = 1
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

