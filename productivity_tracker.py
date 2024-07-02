import time
import csv
import sys


#Timer 

class Task:
    #Creates new task and includes name and category for reporting.
    def __init__(self, name) :
        self.name = name
        self.start_time = None
        self.total_time = 0
    
    # Timer start
    def start(self):
        if self.start_time is None:
            self.start_time = time.time()
    
    # Timer stop
    def stop(self):
        if self.start_time is not None:
            self.total_time += time.time() - self.start_time
            self.start_time = None
    
    # Returns the total time spent on a task.
    def get_time_spent(self):
        if self.start_time is not None:
            return self.total_time + time.time() - self.start_time 
        return self.total_time 

#Task manager

class ProductivityTracker:
    # New task list
    def __init__(self):
        self.tasks = []
    
    # Adding a task
    def add_task(self, name):
        self.tasks.append(Task(name))
        print("Current tasks: ")
        for Task in self.tasks:
            print(f" - {Task.name})")
    
    # Starting the task
    def start_task(self, name):
        for Task in self.tasks:
            if Task.name == name:
                Task.start()
                print(f"Started task: {name}")
                return
            print(f"Task {name} not found.")
    
    # Stopping the task
    def stop_task(self,name):
        for Task in self.tasks:
            if Task.name == name:
                Task.stop()
                print(f"Task {name} stopped.")
                return
            print(f"Task {name} not found.")
    
    # Daily summary
    def daily_summary(self):
        summary = {}
        for task in self.tasks:
            time_spent = task.get_time_spent()
            print("Daily summary:")
            print(f"{task.name}: {time_spent/60:2f} minutes.")
    
    #Exportable CSV report
    def export_csv(self,filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Task Name', 'Time Spent (minutes)'])
            for task in self.tasks:
                writer.writerow([task.name, task.get_time_spent() / 60])
        print(f"Data exported to {filename}")

# User interface

def main():
    tracker = ProductivityTracker()
    
    while True:
        print("Menu:")
        print("1. Add Task")
        print("2. Start Task")
        print("3. Stop Task")
        print("4. Daily Summary")
        print("5. Export to CSV")
        print("6. Exit")
    
        choice = input("Please choose from the Menu options: ")
    
        if choice == '1':
            name = input("Enter task name: ")
            tracker.add_task(name)
        elif choice == '2':
            name = input("Enter task name: ")
            tracker.start_task(name)
            print(f"Task {name} started.")
        elif choice == '3':
            name = input("Enter task name: ")
            tracker.stop_task(name)
            print(f"Task {name} stopped.")
        elif choice == '4':
            tracker.daily_summary()
            print(f"Here is your daily summary.")
        elif choice == '5':
            filename = input("Enter a filename to save your report: ")
            tracker.export_csv(filename)
        elif choice == '6':
            print(f"Exiting the program. Goodbye.")
            sys.exit()
   
    # error handling
        else:
            print(f"Invalid choice. Please choose from option 1 to 5.")
