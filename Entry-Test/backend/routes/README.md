# Flask API - Route Handlers

This module (`routes/__init__.py`) defines the **API routes** for the Flask application, handling **authentication, database connections, and data retrieval**.

## Introduction

The `routes/__init__.py` file is responsible for:
- **Defining API endpoints** using Flask's `Blueprint` feature.
- **Connecting to MySQL** and setting up the database schema.
- **Handling authentication** using JWT-based authentication.
- **Managing API requests** for retrieving industry trend data.

## Features

- **Modular API Blueprint (`api_bp`)**
- **MySQL Database Connection**
- **JWT Authentication & Token-Based Security**
- **Admin Login Endpoint**
- **Industry Trends Data Fetching**
- **Secure Error Handling**

## Database Configuration

During startup, the script prompts for MySQL database credentials:

| Field        | Default Value |
|-------------|--------------|
| Host        | `localhost`   |
| Port        | `3306`        |
| User        | `root`        |
| Password    | `*****`  |
| Database    | `global_outlooks` |

These credentials are stored in `db_config` and used to establish a connection.

### Database Initialization

The script ensures the `admin` table exists before processing any admin login attempts. The schema:

```sql
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    fullname VARCHAR(255) NOT NULL,
    position VARCHAR(255),
    company VARCHAR(255),
    department VARCHAR(255) NOT NULL,
    access_level INT NOT NULL
);
