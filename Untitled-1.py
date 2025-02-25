import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

# File to store tasks
TASKS_FILE = "tasks.txt"

def save_tasks():
    """Save tasks to a file."""
    with open(TASKS_FILE, "w") as file:
        for task in task_list.get_children():
            task_text, time_text = task_list.item(task, "values")
            file.write(f"{task_text},{time_text}\n")

def load_tasks():
    """Load tasks from a file at startup."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            for line in file:
                task_text, time_text = line.strip().split(",")
                task_list.insert("", "end", values=(task_text, time_text))

def add_task():
    """Add a new task to the list."""
    task = task_entry.get()
    time = time_entry.get()
    if task and time:
        task_list.insert("", "end", values=(task, time))
        save_tasks()  # Save after adding
        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task and time.")

def remove_task():
    """Remove selected task from the list."""
    selected_item = task_list.selection()
    if selected_item:
        task_list.delete(selected_item)
        save_tasks()  # Save after removing
    else:
        messagebox.showwarning("Warning", "Please select a task to remove.")

def clear_tasks():
    """Clear all tasks from the list."""
    if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
        for item in task_list.get_children():
            task_list.delete(item)
        save_tasks()  # Save after clearing

# Main App Window
root = tk.Tk()
root.title("To-Do List")
root.geometry("400x400")
root.configure(bg="#f5f5f5")

# Task Entry
frame = tk.Frame(root, bg="#f5f5f5")
frame.pack(pady=10)

task_label = tk.Label(frame, text="Task:", bg="#f5f5f5", font=("Arial", 10))
task_label.grid(row=0, column=0, padx=5, pady=5)
task_entry = tk.Entry(frame, width=25, font=("Arial", 12))
task_entry.grid(row=0, column=1, padx=5, pady=5)

time_label = tk.Label(frame, text="Time:", bg="#f5f5f5", font=("Arial", 10))
time_label.grid(row=1, column=0, padx=5, pady=5)
time_entry = tk.Entry(frame, width=25, font=("Arial", 12))
time_entry.grid(row=1, column=1, padx=5, pady=5)

# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task, font=("Arial", 12), bg="#4CAF50", fg="white")
add_button.pack(pady=5)

remove_button = tk.Button(root, text="Remove Selected", command=remove_task, font=("Arial", 12), bg="#FF5252", fg="white")
remove_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear All", command=clear_tasks, font=("Arial", 12), bg="#FFA500", fg="white")
clear_button.pack(pady=5)

# Task List
columns = ("Task", "Time")
task_list = ttk.Treeview(root, columns=columns, show="headings")
task_list.heading("Task", text="Task")
task_list.heading("Time", text="Time")
task_list.pack(pady=10, fill="both", expand=True)

# Load tasks at startup
load_tasks()

root.mainloop()
