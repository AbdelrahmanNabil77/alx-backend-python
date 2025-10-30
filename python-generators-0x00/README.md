# SQL Streaming with Python Generators

## 📚 About the Project

This project demonstrates how to use Python generators to efficiently stream rows from a SQL database one by one. Instead of loading entire datasets into memory, we use generators to access data lazily — one record at a time — which is particularly useful for handling large datasets or simulating real-time data processing.

In addition to working with generators, the project includes creating and seeding a MySQL database (`ALX_prodev`) with user data from a CSV file.

---

## 🎯 Learning Objectives

Through this project, you will:

- 🔁 **Master Python Generators**  
  Understand and implement Python generator functions using the `yield` keyword to enable lazy iteration.

- 📊 **Handle Large Datasets**  
  Learn to process data in batches or stream it record-by-record without loading the full dataset into memory.

- 🔄 **Simulate Real-world Scenarios**  
  Apply streaming techniques to simulate live updates or real-time data feeds.

- 🚀 **Optimize Performance**  
  Use generators to implement memory-efficient computations such as aggregations (e.g., averages) on large datasets.

- 🧩 **Apply SQL Knowledge**  
  Connect Python to a MySQL database, execute dynamic queries, and integrate results with generator logic.

---

## 🧱 Project Components

- `seed.py`: Contains utility functions to:

  - Connect to MySQL
  - Create the `ALX_prodev` database and `user_data` table
  - Insert data from `user_data.csv`

- `0-main.py`: Entry point that:

  - Runs the seeding process
  - Prints confirmation messages and sample data

- `user_data.csv`: Sample data file used to seed the database

---

## 📦 Requirements

- Python 3.x
- MySQL Server (running locally or remotely)
- [`mysql-connector-python`](https://pypi.org/project/mysql-connector-python/) library:
  ```bash
  pip install mysql-connector-python
  ```
