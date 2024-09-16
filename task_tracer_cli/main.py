import argparse
import os
import json
from datetime import datetime

TASK_FILE = "tasks.json"

#funcion para cargar el archivo
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as f:
            return json.load(f)
    return []
#función para guardar los tasks
def save_tasks(tasks):
    with open(TASK_FILE,'w') as f:
        json.dump(tasks, f, indent=2)

#función para buscar el siguiente id
def get_next_id(tasks):
    return max([task['id'] for task in tasks],default=0 ) + 1

#función para agregar tasks
def add_task(args):
    tasks = load_tasks()
    new_task = {
        "id": get_next_id(tasks),
        "description": args.description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

#función para actualizar tasks
def update_task(args):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == args.id:
            task['description'] = args.description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {args.id} updated successfully")
            return
    print(f"Task with ID {args.id} not found")

#función para borrar los tasks
def delete_task(args):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != args.id]
    save_tasks(tasks)

#Marcar un task in progress o done
def mark_task(args,status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == args.id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {args.id} marked as {status}")
            return
    print(f"Task with ID {args.id} not found")

#funcion para listar todos los tasks
def list_tasks(args):
    tasks = load_tasks()
    if args.status:
        tasks = [task for task in tasks if task['status'] == args.status]
    
    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}")


def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    
     # Add task
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("description")
    add_parser.set_defaults(func=add_task)

    # Update task
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("description")
    update_parser.set_defaults(func=update_task)

    # Delete task
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("id", type=int)
    delete_parser.set_defaults(func=delete_task)

    # Mark task as in-progress
    mark_in_progress_parser = subparsers.add_parser("mark-in-progress")
    mark_in_progress_parser.add_argument("id", type=int)
    mark_in_progress_parser.set_defaults(func=lambda args: mark_task(args, "in-progress"))

    # Mark task as done
    mark_done_parser = subparsers.add_parser("mark-done")
    mark_done_parser.add_argument("id", type=int)
    mark_done_parser.set_defaults(func=lambda args: mark_task(args, "done"))

    # List tasks
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("status", nargs="?", choices=["todo", "in-progress", "done"])
    list_parser.set_defaults(func=list_tasks)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()


