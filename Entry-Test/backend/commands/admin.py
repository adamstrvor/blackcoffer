import mysql.connector
import bcrypt
import os
from termcolor import colored

# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------

def connect_to_db():

    print("\n| DATABASE CONNEXION")
    print("------------------------------------------")

    host = input('|> Provide your MySQL server host: ').strip() or "localhost"
    port = input('|> Provide your MySQL server port: ').strip() or "3306"
    user = input('|> Provide your MySQL username: ').strip() or "root"
    password = input('|> Provide your MySQL password: ').strip() or "Maliba2002"
    database = input('|> Provide the MySQL database name: ').strip() or "global_outlooks"

    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        print(colored("✅ Connected to MySQL database successfully!\n", "green"))
        return conn, cursor
    except mysql.connector.Error as err:
        print(colored(f"❌ MySQL Connection Error: {err}", "red"))
        exit()

# -----------------------------------------
# CHECK & CREATE ADMIN TABLE IF NOT EXISTS
# -----------------------------------------

def setup_admin_table(cursor, conn):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            position VARCHAR(255) NOT NULL,
            company VARCHAR(255),
            department VARCHAR(255) NOT NULL,
            access_level INT NOT NULL
        )
    """)
    conn.commit()
    print(colored("✅ Admin table checked/created successfully!\n", "green"))

# -----------------------------------------
# CHECK IF ANY ADMIN EXISTS
# -----------------------------------------

def is_first_admin(cursor):
    cursor.execute("SELECT COUNT(*) FROM admin")
    count = cursor.fetchone()[0]
    return count == 0

# -----------------------------------------
# REGISTER FIRST ADMIN
# -----------------------------------------

def register_first_admin(cursor, conn):
    print("\n| FIRST ADMIN")
    print("------------------------------------------")
    print(colored("\n🚀 No admins found! Setting up the first admin...\n", "yellow"))

    fullname = input("\t|> Enter Full Name: ").strip()
    email = input("\t|> Enter Email: ").strip()
    password = input("\t|> Enter Password: ").strip()
    position = input("\t|> Enter Position: ").strip()
    company = input("\t|> Enter Company (Optional): ").strip() or None
    department = input("\t|> Enter Department: ").strip()

    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Highest access level (e.g., 10)
    access_level = 10  

    cursor.execute("""
        INSERT INTO admin (fullname, email, password_hash, position, company, department, access_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (fullname, email, password_hash, position, company, department, access_level))

    conn.commit()
    print(colored("✅ First admin registered successfully!\n", "green"))
    return email, access_level

# -----------------------------------------
# ADMIN AUTHENTICATION
# -----------------------------------------

def authenticate_admin(cursor):
    print("\n| AUTHENTICATION")
    print("------------------------------------------")
    while True:
        email = input("|> Enter Admin Email ID: ").strip()
        if email:
            break

    cursor.execute("SELECT id, fullname, password_hash, access_level FROM admin WHERE email = %s", (email,))
    result = cursor.fetchone()

    if not result:
        print(colored("🚨 Connexion refused: Fake attempt detected! ❌", "red"))
        exit()

    admin_id, fullname, stored_hash, access_level = result
    print(colored(f"✅ Admin {fullname} found in the database!", "green"))

    password = input("|> Enter Admin Password: ").strip()

    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        print(colored("✅ Authentication successful! Welcome, Admin! 🎉", "green"))
        return email, access_level
    else:
        print(colored("❌ Authentication failed! Incorrect password.", "red"))
        exit()

# -----------------------------------------
# ADMIN MANAGEMENT OPTIONS
# -----------------------------------------

def add_admin(cursor, conn, highest_level):
    print("\n| NEW ADMIN")
    print("------------------------------------------")
    print(colored("\n🔹 Add New Admin\n", "cyan"))

    fullname = input("\t|> Enter Full Name: ").strip()
    email = input("\t|> Enter Email: ").strip()
    password = input("\t|> Enter Password: ").strip()
    position = input("\t|> Enter Position: ").strip()
    company = input("\t|> Enter Company (Optional): ").strip() or None
    department = input("\t|> Enter Department: ").strip()

    # If highest level admin, allow setting access level
    if highest_level:
        access_level = int(input("\t|> Enter Access Level (1-10): ").strip() or 5)
    else:
        access_level = 5  # Standard access level

    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cursor.execute("""
        INSERT INTO admin (fullname, email, password_hash, position, company, department, access_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (fullname, email, password_hash, position, company, department, access_level))

    conn.commit()
    print(colored("✅ Admin added successfully!\n", "green"))

def update_admin(cursor, conn, highest_level):
    print("\n| UPDATE ADMIN")
    print("------------------------------------------")
    print(colored("\n🔹 Update Admin data along with the access Level\n", "cyan"))


    if highest_level:
        email = input("\t|> Enter Email: ").strip()
        fullname = input("\t|> Enter Full Name: ").strip()
        position = input("\t|> Enter Position: ").strip()
        company = input("\t|> Enter Company (Optional): ").strip() or None
        department = input("\t|> Enter Department: ").strip()
        new_access_level = int(input("|> Enter New Access Level (1-10): ").strip())


        cursor.execute("UPDATE admin SET fullname = %s, position = %s, company = %s, department = %s, access_level = %s WHERE email = %s", (fullname, position, company, department, new_access_level, email ))
        conn.commit()

        print(colored("✅ Admin data updated successfully!\n", "green"))
    else:
        print(colored("❌ Sorry, even though you're admin only the super admin can update your details!\n", "red"))

# -----------------------------------------
# MAIN FUNCTION
# -----------------------------------------

def main():
    print("\n------------------------------------------")
    print("| WECLOME ON THE ADMIN COMMAND LINE INTERFACE (CLI)")
    print("------------------------------------------")
    conn, cursor = connect_to_db()
    setup_admin_table(cursor, conn)

    if is_first_admin(cursor):
        admin_email, admin_access_level = register_first_admin(cursor, conn)
    else:
        admin_email, admin_access_level = authenticate_admin(cursor)

    highest_level = admin_access_level == 10

    while True:
        print("\n🔹 Admin Management Options:")
        print("1️⃣ Add Admin")
        print("2️⃣ Update Admin")
        print("3️⃣ Exit")
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_admin(cursor, conn, highest_level)
        elif choice == "2":
            if highest_level:
                update_admin(cursor, conn, highest_level)
            else:
                print(colored("❌ Only highest-level admin can update access levels.", "red"))
        elif choice == "3":
            print(colored("\n🔒 Exiting admin management.", "yellow"))
            break

    cursor.close()
    conn.close()

# Run script
if __name__ == "__main__":
    main()
