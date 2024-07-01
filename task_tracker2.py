import argparse
import csv
import datetime
import os
import time

TASKS_FILE = 'tasks.csv'

class Task:
    def __init__(self, name, start_time, end_time=None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time

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

def start_task(task_name):
    tasks = load_tasks()
    tasks.append(Task(task_name, time.time()))
    save_tasks(tasks)
    print(f"Started task: {task_name}")

def stop_task(task_name):
    tasks = load_tasks()
    for task in tasks:
        if task.name == task_name and task.end_time is None:
            task.end_time = time.time()
            save_tasks(tasks)
            print(f"Stopped task: {task_name}")
            return
    print(f"Task not found or already stopped: {task_name}")

def daily_summary():
    tasks = load_tasks()
    today = datetime.date.today()
    summary = []
    for task in tasks:
        start_date = datetime.datetime.fromtimestamp(task.start_time).date()
        if start_date == today:
            duration = (task.end_time - task.start_time) if task.end_time else (time.time() - task.start_time)
            summary.append({
                'name': task.name,
                'duration': duration,
            })
    for entry in summary:
        print(f"Task: {entry['name']}, Duration: {entry['duration']/60:.2f} minutes")

def export_csv():
    tasks = load_tasks()
    with open('tasks_export.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'start_time', 'end_time', 'duration']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow({
                'name': task.name,
                'start_time': datetime.datetime.fromtimestamp(task.start_time).isoformat(),
                'end_time': datetime.datetime.fromtimestamp(task.end_time).isoformat() if task.end_time else '',
                'duration': (task.end_time - task.start_time) if task.end_time else (time.time() - task.start_time),
            })
    print("Exported tasks to tasks_export.csv")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker")
    parser.add_argument('command', choices=['start', 'stop', 'summary', 'export'], help='Command to execute')
    parser.add_argument('--name', help='Name of the task')

    args = parser.parse_args()

    if args.command == 'start' and args.name:
        start_task(args.name)
    elif args.command == 'stop' and args.name:
        stop_task(args.name)
    elif args.command == 'summary':
        daily_summary()
    elif args.command == 'export':
        export_csv()
    else:
        print("Invalid command or missing task name")

if __name__ == "__main__":
    main()
