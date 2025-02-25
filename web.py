import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import os

# File to store tasks
TASKS_FILE = "tasks.txt"

PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3}  # Sorting order

def save_tasks():
    """Save tasks to a file."""
    with open(TASKS_FILE, "w") as file:
        for task in task_list.get_children():
            values = task_list.item(task, "values")
            file.write(",".join(values) + "\n")

def load_tasks():
    """Load tasks from a file at startup and sort them."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = []
            for line in file:
                parts = line.strip().split(",", maxsplit=4)  # Ensures correct splitting
                if len(parts) == 5:
                    tasks.append(parts)
            tasks.sort(key=lambda x: PRIORITY_ORDER.get(x[2], 3))  # Sort by priority
            for task in tasks:
                task_list.insert("", "end", values=task)
        update_row_colors()

def add_task():
    """Add a new task to the list and sort by priority."""
    task = task_entry.get().strip()
    time = time_entry.get().strip()
    priority = priority_var.get().strip()
    due_date = date_entry.get().strip()
    description = description_entry.get().strip()

    if task and time and priority and due_date:
        task_list.insert("", "end", values=(task, time, priority, due_date, description))
        sort_tasks()  # Sort tasks after adding
        save_tasks()
        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter all task details.")

def remove_task():
    """Remove selected task from the list."""
    selected_item = task_list.selection()
    if selected_item:
        task_list.delete(selected_item)
        save_tasks()
        update_row_colors()
    else:
        messagebox.showwarning("Warning", "Please select a task to remove.")

def clear_tasks():
    """Clear all tasks from the list."""
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
        for item in task_list.get_children():
            task_list.delete(item)
        save_tasks()

def sort_tasks():
    """Sort tasks by priority (High → Medium → Low)."""
    tasks = [(task_list.item(task, "values"), task) for task in task_list.get_children()]
    tasks.sort(key=lambda x: PRIORITY_ORDER.get(x[0][2], 3))  # Sort by priority

    for i, (values, task) in enumerate(tasks):
        task_list.move(task, "", i)  # Reorder tasks in the Treeview

    update_row_colors()  # Refresh row colors

def update_row_colors():
    """Update row colors to visually differentiate tasks."""
    for i, task in enumerate(task_list.get_children()):
        priority = task_list.item(task, "values")[2]  # Get priority
        if priority == "High":
            task_list.item(task, tags=("high_priority",))
        elif i % 2 == 0:
            task_list.item(task, tags=("even_row",))
        else:
            task_list.item(task, tags=("odd_row",))
    
    task_list.tag_configure("high_priority", background="#ffcccc")  # Light Red for High
    task_list.tag_configure("even_row", background="#f0f0f0")  # Light Gray
    task_list.tag_configure("odd_row", background="white")  # White for contrast

# Main App Window
root = tk.Tk()
root.title("To-Do List")
root.geometry("600x450")
root.configure(bg="#f5f5f5")

# Task Entry Frame
frame = tk.Frame(root, bg="#f5f5f5")
frame.pack(pady=10)

# Labels and Entry Fields
task_label = tk.Label(frame, text="Task:", bg="#f5f5f5", font=("Arial", 10))
task_label.grid(row=0, column=0, padx=5, pady=5)
task_entry = tk.Entry(frame, width=25, font=("Arial", 12))
task_entry.grid(row=0, column=1, padx=5, pady=5)

time_label = tk.Label(frame, text="Time:", bg="#f5f5f5", font=("Arial", 10))
time_label.grid(row=1, column=0, padx=5, pady=5)
time_entry = tk.Entry(frame, width=25, font=("Arial", 12))
time_entry.grid(row=1, column=1, padx=5, pady=5)

priority_label = tk.Label(frame, text="Priority:", bg="#f5f5f5", font=("Arial", 10))
priority_label.grid(row=2, column=0, padx=5, pady=5)
priority_var = ttk.Combobox(frame, values=["High", "Medium", "Low"], state="readonly")
priority_var.grid(row=2, column=1, padx=5, pady=5)
priority_var.set("Medium")  # Default selection

date_label = tk.Label(frame, text="Due Date:", bg="#f5f5f5", font=("Arial", 10))
date_label.grid(row=3, column=0, padx=5, pady=5)
date_entry = DateEntry(frame, width=22, background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=3, column=1, padx=5, pady=5)

description_label = tk.Label(frame, text="Description:", bg="#f5f5f5", font=("Arial", 10))
description_label.grid(row=4, column=0, padx=5, pady=5)
description_entry = tk.Entry(frame, width=25, font=("Arial", 12))
description_entry.grid(row=4, column=1, padx=5, pady=5)

# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task, font=("Arial", 12), bg="#4CAF50", fg="white")
add_button.pack(pady=5)

remove_button = tk.Button(root, text="Remove Selected", command=remove_task, font=("Arial", 12), bg="#FF5252", fg="white")
remove_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear All", command=clear_tasks, font=("Arial", 12), bg="#FFA500", fg="white")
clear_button.pack(pady=5)

# Task List
columns = ("Task", "Time", "Priority", "Due Date", "Description")
task_list = ttk.Treeview(root, columns=columns, show="headings", height=10)
task_list.heading("Task", text="Task")
task_list.heading("Time", text="Time")
task_list.heading("Priority", text="Priority")
task_list.heading("Due Date", text="Due Date")
task_list.heading("Description", text="Description")
task_list.pack(pady=10, fill="both", expand=True)

# Load tasks at startup
load_tasks()

root.mainloop()
