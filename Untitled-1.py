import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def add_task():
    task = task_entry.get()
    time = time_entry.get()
    if task and time:
        task_list.insert("", "end", values=(task, time))
        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task and time.")

def remove_task():
    selected_item = task_list.selection()
    if selected_item:
        task_list.delete(selected_item)
    else:
        messagebox.showwarning("Warning", "Please select a task to remove.")

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

# Task List
columns = ("Task", "Time")
task_list = ttk.Treeview(root, columns=columns, show="headings")
task_list.heading("Task", text="Task")
task_list.heading("Time", text="Time")
task_list.pack(pady=10, fill="both", expand=True)

root.mainloop()
