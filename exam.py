import datetime
import time
from threading import Thread

# fifo logs and data initialize
task_list = []
fifo_logs = []
fifo_datas = []
fichier = open("exam.txt", "a")
global_start_time = datetime.datetime.now()
running_thread = Thread()

def get_first_execution_time_task_in_list(given_list):
    if len(given_list) > 0:
        sorted_by_next_execution_time = sorted(given_list, key=lambda x: x.next_execution)
        return sorted_by_next_execution_time[0]
    else:
        return None

def launch_next_task():
    global running_thread
    lowest_time_task_of_each_list = [get_first_execution_time_task_in_list(task_list), get_first_execution_time_task_in_list(fifo_datas), get_first_execution_time_task_in_list(fifo_logs)]
    last_list = []
    for task in lowest_time_task_of_each_list:
        if task != None:
            last_list.append(task)
    
    task_with_lowest_execution_time = get_first_execution_time_task_in_list(last_list)

    if (task_with_lowest_execution_time.next_execution <= datetime.datetime.now() and running_thread.is_alive() == False and task_with_lowest_execution_time.next_execution >= datetime.datetime.now() - datetime.timedelta(0,5) ):
        running_thread = task_with_lowest_execution_time
        running_thread.run()
    elif(task_with_lowest_execution_time.next_execution <= datetime.datetime.now() - datetime.timedelta(0,1)):
        task_with_lowest_execution_time.next_execution = datetime.datetime.now() + datetime.timedelta(0, 2)
        print('Time passed for task: '+ str(task_with_lowest_execution_time))

class my_task(Thread):
    name = None
    period  = None
    execution_time = None
    next_execution = None
    logs_write = False 
    datas_write = False

    
    def __init__(self, name, period, execution_time, next_execution, logs_write=False, datas_write=False):
        Thread.__init__(self)
        self.name = name
        self.period = period
        self.execution_time = execution_time
        self.next_execution = next_execution
        self.logs_write = logs_write
        self.datas_write = datas_write

    
    def run(self):
        print(datetime.datetime.now().strftime("%H:%M:%S") +
                "\t" + self.name + " : Starting task tank")
        fichier.write(datetime.datetime.now().strftime(
            "%H:%M:%S") + "\t" + self.name + " : Starting task tank" + "\n")
        

    
    def sleep(self):
        time.sleep(self.execution_time)

       
        print(datetime.datetime.now().strftime("%H:%M:%S") + "\t" + self.name + " : Task tank is done")
        fichier.write(datetime.datetime.now().strftime("%H:%M:%S") + "\t" + self.name + " : Task tank is done" + "\n")
        
       
        self.next_execution = datetime.datetime.now() + datetime.timedelta(0, self.period)
        


if __name__ == '__main__':

    
    task_list.append(my_task(name="Pump1", period=5, execution_time=2, next_execution=global_start_time + datetime.timedelta(0, 5), logs_write=True, datas_write=True))
    task_list.append(my_task(name="Pump2", period=15, execution_time=3, next_execution=global_start_time + datetime.timedelta(0, 15), logs_write=True))
    task_list.append(my_task(name="Machine1", period=5, execution_time=5, next_execution=global_start_time + datetime.timedelta(0, 5), logs_write=True))
    task_list.append(my_task(name="Machine2", period=5, execution_time=3, next_execution=global_start_time + datetime.timedelta(0, 5), logs_write=True))
    
    
    while(1):
        print('tank')
        launch_next_task()
        time.sleep(1)