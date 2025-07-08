s# Seed Script: MySQL Database Setup and Population

This script (`seed.py`) automates the creation and seeding of a MySQL database named **ALX_prodev** using sample data from a CSV file.

---

## 📦 Features

- ✅ Connects to the MySQL server
- ✅ Creates the database `ALX_prodev` (if it doesn't exist)
- ✅ Creates the `user_data` table (if it doesn't exist)
- ✅ Populates the table from a CSV file (`user_data.csv`)
- ✅ Skips duplicate entries (based on `user_id`)
- ✅ Uses UUID as primary key

---

## 🛠️ Requirements

- Python 3.x
- MySQL server running locally
- Python packages:
  - `mysql-connector-python`

Install required package:
```bash
pip install mysql-connector-python
