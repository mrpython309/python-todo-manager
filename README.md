# 📋 Smart Task Manager & To-Do List Application

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![UI](https://img.shields.io/badge/UI-Desktop%20%26%20Web-purple.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)

A modular, object-oriented **Task Management Application** built using **Python 3**. This project demonstrates clean software architecture, JSON data serialization, persistent storage, custom exception handling, and offers both a **Modern Web UI** and a **Desktop Tkinter GUI**.

---

## ✨ Features

- **Dual Interfaces**: Choose between a modern **Responsive Web UI** or a **Desktop Tkinter GUI**.
- **Full CRUD Operations**: Create, Read, Update (Mark Complete), and Delete tasks effortlessly.
- **Task Prioritization & Categorization**: Organize tasks with High, Medium, and Low priorities across Work, Personal, Study, or General categories.
- **Persistent Storage**: Automatic state retention using **JSON file serialization** (`tasks.json`).
- **Custom Exception Handling**: Enforces input validation and structured exception propagation (`TaskNotFoundError`).
- **Zero External Dependencies**: Runs out-of-the-box using standard Python standard libraries (`http.server`, `json`, `tkinter`).
- **Automated Unit Testing**: Includes comprehensive test suites using Python's built-in `unittest` framework.

---

## 🚀 Quick Start & Usage

### 1️⃣ Run the Web UI Application (Recommended)
Launch a local Web Server that automatically opens the interactive Web UI in your default browser:
```bash
python app.py
```
> Access at: `http://localhost:5000`

### 2️⃣ Run the Desktop Tkinter GUI Application
Launch a standalone desktop GUI window:
```bash
python gui_todo.py
```

### 3️⃣ Run CLI / Terminal Version
Run the interactive command-line interface:
```bash
python todo_manager.py
```

---

## 🧪 Running Unit Tests

To verify all business logic, persistence, and exception handling:
```bash
python -m unittest test_todo.py
```

---

## 📂 Project Architecture

```
python-todo-manager/
│
├── app.py              # Web Application server & REST API (HTML/CSS/JS frontend)
├── gui_todo.py         # Desktop GUI application (Tkinter)
├── todo_manager.py     # Core OOP business logic & CLI interface
├── test_todo.py        # Automated Unit Test suite
├── tasks.json          # Persistent JSON storage file
└── README.md           # Project documentation
```

---

## 🛠️ Key Python Concepts Demonstrated

- **Object-Oriented Programming (OOP)**: Clean encapsulation with `Task` and `TaskManager` classes.
- **Data Serialization**: Converting Python objects to/from JSON dictionary structures (`to_dict` / `from_dict`).
- **File I/O & Context Managers**: Safe file operations with `with open(...) as f:`.
- **RESTful API Principles**: HTTP GET/POST handling with standardized JSON payloads.
- **Unit Testing**: Test-Driven Development (TDD) principles using `unittest`.

---

## 👤 Author

**Anees Shaikh**
- **GitHub**: [@mrpython309](https://github.com/mrpython309)
- **LinkedIn**: [Anees Shaikh](https://linkedin.com/in/anees-shaikh-a7451a295)
- **Email**: shaikhanees841@gmail.com
