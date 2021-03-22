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
        self.curr_tid = -1;
        self.tasks_completed = 0
        self.tasks_missed = 0
        
    def get_task_from_id(self, tid):
        for task in task_set:
            if task.tid == tid:
                return task
        return None

    def schedule(self, t):
        for task in task_set:
            # task enters ready state once it has exceeded its period
            if t == task.next_allowed_task:
                task.ready = True
        
        task_list = [task for task in task_set if task.ready]
        
        #sort ready tasks
        task_list = get_earliest_deadline_task_list(task_list)
        tid = []
        for task in task_list:
           tid.append(task.tid)
        #print('>>>>')
        #print('T={} {}'.format(t, tid))
    
        self.update_tasks(task_list, t)
        
        for task in task_set:
            if task.next_deadline == t:
                if not task.completed:
                    print('Task {} deadline missed.'.format(task.tid))
                    self.tasks_missed += 1
                task.completed = False
                task.next_deadline += task.period
                task.progress = 0
                print('Task {} has reached its deadline of T={}. The new deadline is T={}'.format(task.tid, (task.next_deadline-task.period), task.next_deadline))
        
        #print('----')
        
    def update_tasks(self, task_list, t):
            #scheduler is idle if task_list is empty
        if not task_list:
            print('Scheduler is idle at T={}'.format(t))
            self.curr_tid = -1
            return
        # starting case
        if self.curr_tid == -1:
            #print('Task {} start at T={}'.format(task_list[0].tid, t))
            task_list[0].job_start = t
        elif self.curr_tid != task_list[0].tid:
            print('Task {} preempted Task {} at T={}'.format(task_list[0].tid, self.curr_tid, t))
            preempted_task = self.get_task_from_id(self.curr_tid)
            preempted_task.num_preemptions += 1
            if task_list[0].job_start == -1:
                task_list[0].job_start = t
                print('Task {} started at T={}.'.format(task_list[0].tid, t))
            else:
                print('Task {} resuming execution at T={}.'.format(task_list[0].tid, t)) 
        
        self.curr_tid = task_list[0].tid
        completed_task_flag = False
        #add progress to earliest deadline task
        task_list[0].progress += 1
          
        #print('Task {} progress: {} wcet: {}'.format(task_list[0].tid, task_list[0].progress, task_list[0].wcet))
        if task_list[0].progress == task_list[0].wcet:
            self.tasks_completed += 1
            if task_list[0].num_preemptions == 0:
                print('Task {} completed execution from T={} to T={}.'.format(task_list[0].tid, task_list[0].job_start, t))
            else:
                print('Task {} completed execution from T={} to T={} with {} preemption(s).'.format(task_list[0].tid, task_list[0].job_start, t, task_list[0].num_preemptions))
            task_list[0].completed = True
            task_list[0].ready = False
            task_list[0].num_jobs_completed += 1
            task_list[0].job_start = -1
            task_list[0].next_allowed_task += task_list[0].period
            task_list[0].num_preemptions = 0
            completed_task_flag = True
            self.curr_tid = -1
        
        # start second job
        if completed_task_flag:
            if len(task_list) >1:
                self.curr_tid = task_list[1].tid
                task_list[1].progress +=1
                
                if task_list[1].job_start == -1:
                    task_list[1].job_start = t
                    print('Task {} started at T={}.'.format(task_list[1].tid, t))
                else:
                    print('Task {} resuming execution at T={}.'.format(task_list[1].tid, t))
            else:
                self.curr_tid = -1
                print('Scheduler is idle at T={}'.format(t))
                return
        
    
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

