"""
Smart Task Manager & To-Do Application (GUI Version)
Author: Anees Shaikh
Description: Modern Tkinter Desktop GUI for Task Management with JSON persistence.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Manager — Python 3")
        self.root.geometry("750x550")
        self.root.minsize(700, 500)
        self.root.configure(bg="#f4f5f7")

        self.storage_file = "tasks.json"
        self.tasks = []
        self.next_id = 1

        self.setup_styles()
        self.create_widgets()
        self.load_tasks()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure Colors
        style.configure("TFrame", background="#f4f5f7")
        style.configure("Header.TLabel", font=("Inter", 16, "bold"), background="#1e293b", foreground="#ffffff", padding=12)
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Primary.TButton", font=("Inter", 9, "bold"), background="#2563eb", foreground="#ffffff", borderwidth=0, padding=6)
        style.map("Primary.TButton", background=[("active", "#1d4ed8")])
        style.configure("Danger.TButton", font=("Inter", 9, "bold"), background="#dc2626", foreground="#ffffff", borderwidth=0, padding=6)
        style.map("Danger.TButton", background=[("active", "#b91c1c")])

    def create_widgets(self):
        # Header Banner
        header = tk.Label(
            self.root, 
            text="📋 Smart Task Manager & To-Do List", 
            font=("Segoe UI", 16, "bold"), 
            bg="#0f172a", 
            fg="#ffffff", 
            anchor="w", 
            padx=20, 
            pady=12
        )
        header.pack(fill="x")

        # Main Container
        main_frame = tk.Frame(self.root, bg="#f4f5f7", padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)

        # Input Card Frame
        input_card = tk.LabelFrame(main_frame, text=" Add New Task ", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#1e293b", padx=15, pady=10, relief="solid", bd=1)
        input_card.pack(fill="x", pady=(0, 10))

        # Row 1: Title
        tk.Label(input_card, text="Task Title:", font=("Segoe UI", 9, "bold"), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=4)
        self.title_entry = ttk.Entry(input_card, width=35, font=("Segoe UI", 9))
        self.title_entry.grid(row=0, column=1, sticky="w", padx=10, pady=4)

        # Category
        tk.Label(input_card, text="Category:", font=("Segoe UI", 9, "bold"), bg="#ffffff").grid(row=0, column=2, sticky="w", pady=4)
        self.category_cb = ttk.Combobox(input_card, values=["General", "Work", "Personal", "Study"], width=12, state="readonly")
        self.category_cb.set("General")
        self.category_cb.grid(row=0, column=3, sticky="w", padx=10, pady=4)

        # Row 2: Priority & Add Button
        tk.Label(input_card, text="Priority:", font=("Segoe UI", 9, "bold"), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=4)
        self.priority_cb = ttk.Combobox(input_card, values=["High", "Medium", "Low"], width=12, state="readonly")
        self.priority_cb.set("Medium")
        self.priority_cb.grid(row=1, column=1, sticky="w", padx=10, pady=4)

        add_btn = tk.Button(input_card, text="+ Add Task", command=self.add_task, bg="#2563eb", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=15, pady=4, cursor="hand2")
        add_btn.grid(row=1, column=3, sticky="e", padx=10, pady=4)

        # Controls & Filter Bar
        control_frame = tk.Frame(main_frame, bg="#f4f5f7")
        control_frame.pack(fill="x", pady=6)

        tk.Label(control_frame, text="Filter:", font=("Segoe UI", 9, "bold"), bg="#f4f5f7").pack(side="left", padx=4)
        self.filter_cb = ttk.Combobox(control_frame, values=["All Tasks", "Pending", "Completed"], width=12, state="readonly")
        self.filter_cb.set("All Tasks")
        self.filter_cb.pack(side="left", padx=4)
        self.filter_cb.bind("<<ComboboxSelected>>", lambda e: self.render_tasks())

        complete_btn = tk.Button(control_frame, text="✓ Mark Completed", command=self.complete_task, bg="#16a34a", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=2, cursor="hand2")
        complete_btn.pack(side="right", padx=4)

        delete_btn = tk.Button(control_frame, text="🗑 Delete Selected", command=self.delete_task, bg="#dc2626", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=2, cursor="hand2")
        delete_btn.pack(side="right", padx=4)

        # Task Table (Treeview)
        table_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, pady=6)

        columns = ("id", "status", "title", "category", "priority", "created")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("status", text="Status")
        self.tree.heading("title", text="Task Title")
        self.tree.heading("category", text="Category")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("created", text="Created At")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("title", width=260, anchor="w")
        self.tree.column("category", width=90, anchor="center")
        self.tree.column("priority", width=80, anchor="center")
        self.tree.column("created", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_task(self):
        title = self.title_entry.get().strip()
        category = self.category_cb.get()
        priority = self.priority_cb.get()

        if not title:
            messagebox.showwarning("Input Error", "Please enter a valid task title.")
            return

        task = {
            "task_id": self.next_id,
            "title": title,
            "category": category,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()
        self.render_tasks()
        self.title_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Task #{task['task_id']} added successfully!")

    def complete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task from the list.")
            return

        item = self.tree.item(selected[0])
        task_id = item["values"][0]

        for t in self.tasks:
            if t["task_id"] == task_id:
                t["completed"] = True
                break

        self.save_tasks()
        self.render_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task from the list.")
            return

        item = self.tree.item(selected[0])
        task_id = item["values"][0]

        if messagebox.askyesno("Confirm Delete", f"Delete task #{task_id}?"):
            self.tasks = [t for t in self.tasks if t["task_id"] != task_id]
            self.save_tasks()
            self.render_tasks()

    def render_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filter_val = self.filter_cb.get()

        for t in self.tasks:
            if filter_val == "Pending" and t["completed"]:
                continue
            if filter_val == "Completed" and not t["completed"]:
                continue

            status_str = "✓ Done" if t["completed"] else "⏳ Pending"
            self.tree.insert("", "end", values=(
                t["task_id"],
                status_str,
                t["title"],
                t["category"],
                t["priority"],
                t["created_at"]
            ))

    def save_tasks(self):
        data = {"next_id": self.next_id, "tasks": self.tasks}
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_tasks(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.next_id = data.get("next_id", 1)
                    self.tasks = data.get("tasks", [])
            except Exception as e:
                print(f"Error loading tasks: {e}")
        self.render_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
