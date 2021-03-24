# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 19:26:22 2021

@author: eleojjz
"""
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
        self.ready = True
        
        split = details.split(',')
        self.tid = idx
        self.wcet = int(split[0])
        self.next_deadline = int(split[1])
        self.period = int(split[1])
    
    def print_details(self):
        print('Task ID: ' + str(self.tid) + ' WCET: ' + str(self.wcet) + 
              ' Deadline: ' + str(self.next_deadline) + 
              ' Period: ' + str(self.period))
    
    def get_laxity(self, t):
        return (self.next_deadline - t) - (self.wcet-self.progress)

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
        self.task_start = 0
        self.tasks_completed = 0
        self.tasks_missed = 0

    def schedule(self, t, is_last):
        for task in task_set:
            if task.tid == self.curr_tid:
                task.progress += 1
                if task.progress == task.wcet:
                    task.completed = True
                    task.ready = False
                    task.num_jobs_completed += 1
                    self.tasks_completed += 1
                    print('Task {} completed.'.format(task.tid))
            
            if task.next_deadline == t:
                if not task.completed:
                    task.num_jobs_missed += 1
                    self.tasks_missed += 1
                    print('Deadline for task {} is missed at T={}.'.format(task.tid, t))
                task.next_deadline += task.period
                task.progress = 0
                task.completed = False
                task.ready = True
            
            
            task_lax = task.get_laxity(t)
            if task_lax == 0:
                print('T={} Task {} has reached zero laxity'.format(t, task.tid))
                print('..........')
        
        task_list = [task for task in task_set if task.ready]
        task_list = get_earliest_deadline_task_list(task_list)
        #print final message at the last iteration
        if is_last:
            if self.curr_tid != -1:
                print('Task {} ran from T={} to T={}'.format(self.curr_tid, self.task_start, t))
            else:
                print('Scheduler is idle from T={} to T={}'.format(self.task_start, t))
            return
            
        if not task_list:
            if self.curr_tid != -1:
                print('Task {} ran from T={} to T={}'.format(self.curr_tid, self.task_start, t))
                self.task_start = t
                self.curr_tid = -1
        elif self.curr_tid != task_list[0].tid:
            if self.curr_tid != -1:
                print('Task {} ran from T={} to T={}'.format(self.curr_tid, self.task_start, t))
            else:
                if self.task_start != t:
                    print('Scheduler is idle from T={} to T={}'.format(self.task_start, t))
            self.task_start = t
            self.curr_tid = task_list[0].tid
        
        
    
    def run(self, duration):
        t = 0;
        while t <= duration:
            is_last = False
            if t == duration:
                is_last = True
            self.schedule(t, is_last)
            t += 1
        
        self.print_simulation_report()
    
    def print_simulation_report(self):
        
        print('Simulation Complete.')
        print('Simulation Report')
        print('----------------------------------------------')
        print('Task ID | # Executed | # Completed | # Missed')
        for task in task_set:
            print('{} | {} | {} | {}'.format(task.tid, (task.num_jobs_missed+task.num_jobs_completed), task.num_jobs_completed, task.num_jobs_missed))
        
        print('Tasks completed: {}.'.format(self.tasks_completed))
        print('Tasks missed: {}.'.format(self.tasks_missed))
        
        
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

