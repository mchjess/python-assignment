
#tasks
import time
import os
import csv

TASKS_FILE = 'tasks.csv'

class Task:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.start_time = None
        self.total_time = 0
    python task_tracker.py start --name "Task Name"
    @classmethod
    def from_csv(cls, row):
        start_time = float(row[1])
        end_time = float(row[2]) if row[2] else None
        return cls(row[0], start_time, end_time)

    def to_csv(self):
        return [self.name, str(self.start_time), str(self.end_time) if self.end_time else '']

    def load_tasks():
        if not os.path.exists(TASKS_FILE):
            return []
        with open(TASKS_FILE, 'r') as file:
            reader = csv.reader(file)
            return [Task.from_csv(row) for row in reader]

    def save_tasks(tasks):
        with open(TASKS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            for task in tasks:
                 writer.writerow(task.to_csv())

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is not None:
            self.total_time += time.time() - self.start_time
            self.start_time = None

    def get_time_spent(self):
        return self.total_time if self.start_time is None else self.total_time + time.time() - self.start_time
    
    
 #tracker 
import csv

class ProductivityTracker:
    
     def list_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        for task in self.tasks:
            print(f"Task: {task.name}, Category: {task.category}, Time Spent: {task.get_time_spent() / 60:.2f} minutes")
            
     def __init__(self):
        self.tasks = []

     def add_task(self, name, category):
        self.tasks.append(Task(name, category))

     def start_task(self, name):
        for task in self.tasks:
            if task.name == name:
                task.start()
                print(f"Started task: {name}")
                return
        print(f"Task {name} not found.")

     def stop_task(self, name):
        for task in self.tasks:
            if task.name == name:
                task.stop()
                print(f"Stopped task: {name}")
                return
        print(f"Task {name} not found.")

     def daily_summary(self):
        summary = {}
        for task in self.tasks:
            time_spent = task.get_time_spent()
            if task.category in summary:
                summary[task.category] += time_spent
            else:
                summary[task.category] = time_spent
        
        print("Daily Summary:")
        for category, time_spent in summary.items():
            print(f"{category}: {time_spent/60:.2f} minutes")

     def export_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Task Name', 'Category', 'Time Spent (minutes)'])
            for task in self.tasks:
                writer.writerow([task.name, task.category, task.get_time_spent()/60])
        print(f"Data exported to {filename}")

#command line interface
import sys

if __name__ == "__main__":
    tracker = ProductivityTracker()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--add":
            if len(sys.argv) >= 4:
                name = sys.argv[2]
                category = sys.argv[3]
                tracker.add_task(name, category)
                print(f"Added task: {name}")
            else:
                print("Usage: python productivity_tracker.py --add <name> <category>")
        
        elif command == "--start":
            if len(sys.argv) >= 3:
                name = sys.argv[2]
                tracker.start_task(name)
            else:
                print("Usage: python productivity_tracker.py --start <name>")
        
        elif command == "--stop":
            if len(sys.argv) >= 3:
                name = sys.argv[2]
                tracker.stop_task(name)
            else:
                print("Usage: python productivity_tracker.py --stop <name>")
        
        elif command == "--summary":
            tracker.daily_summary()
        
        elif command == "--export":
            if len(sys.argv) >= 3:
                filename = sys.argv[2]
                tracker.export_csv(filename)
                print(f"Data exported to {filename}")
            else:
                print("Usage: python productivity_tracker.py --export <filename>")
        
        elif command == "--list":
            tracker.list_tasks()
        
        else:
            print("Invalid command. Use --add, --start, --stop, --summary, --export, or --list.")
    else:
        print("Usage: python productivity_tracker.py [--add <name> <category> | --start <name> | --stop <name> | --summary | --export <filename> | --list]")