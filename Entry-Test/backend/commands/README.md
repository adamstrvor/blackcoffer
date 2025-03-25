# Command Line Interface (CLI) for Database Management

This repository contains Python scripts for managing MySQL databases, including dataset loading and admin user management.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Loading Datasets (`load.py`)](#loading-datasets-loadpy)
  - [Admin Management (`admin.py`)](#admin-management-adminpy)
- [License](#license)

## Overview
This CLI provides an interactive interface for managing datasets and user administration in a MySQL database. It includes:
- **`load.py`**: A script to load various datasets (CSV, JSON, Excel, etc.) into a MySQL database.
- **`admin.py`**: A script for setting up and managing admin users, including authentication and access level control.

## Requirements
Ensure you have the following installed:
- Python 3.x
- MySQL Server
- Required Python libraries:
  ```sh
  pip install mysql-connector-python pandas openpyxl termcolor bcrypt
  ```

## Installation
Clone this repository and navigate into the project directory:
```sh
git clone https://github.com/adamstrvor/blackcoffer
cd https://github.com/adamstrvor/blackcoffer
```

## Usage

### Loading Datasets (`load.py`)
The `load.py` script allows users to load structured datasets into a MySQL database.

#### Steps to Use:
1. Run the script:
   ```sh
   python commands/load.py
   ```
2. Enter MySQL credentials and database details.
3. Provide the dataset path and file name.
4. The script will:
   - Load the dataset (supports CSV, JSON, Excel, Parquet, HTML, Pickle).
   - Create a table if it does not exist.
   - Insert the dataset into the specified table.
5. Optionally, repeat the process for multiple datasets.

### Admin Management (`admin.py`)
The `admin.py` script allows secure management of admin users in the MySQL database.

#### Features:
- Connects to a MySQL database.
- Checks if an admin table exists and creates one if necessary.
- Registers the first admin with the highest access level.
- Authenticates existing admins using email and password.
- Allows super admins to add or update admin users.

#### Steps to Use:
1. Run the script:
   ```sh
   python commands/admin.py
   ```
2. Enter MySQL credentials.
3. If no admin exists, register the first admin.
4. Authenticate using admin credentials.
5. Choose from options:
   - Add new admins.
   - Update admin details (only for super admins).
6. Exit when done.

## License
This project is licensed under the MIT License.

