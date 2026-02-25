import os

STUDENT_FILE = "students.txt"
LOGIN_FILE = "login.txt"

ADMIN_USER = "admin"
ADMIN_PASS = "1234"


# ------------------ DATA HELPERS ------------------

def load_students():
    students = {}
    if not os.path.exists(STUDENT_FILE):
        return students

    with open(STUDENT_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 6:
                continue

            sid, name, email, phone, dept, grade = parts
            students[int(sid)] = {
                "name": name,
                "email": email,
                "phone": phone,
                "department": dept,
                "grade": float(grade)
            }

    return students


def save_students(students):
    with open(STUDENT_FILE, "w") as f:
        for sid, data in students.items():
            f.write(f"{sid}|{data['name']}|{data['email']}|{data['phone']}|{data['department']}|{data['grade']}\n")


def load_logins():
    logins = {}
    if not os.path.exists(LOGIN_FILE):
        return logins

    with open(LOGIN_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sid, pwd = line.split(",")
            logins[int(sid)] = pwd

    return logins


def save_logins(logins):
    with open(LOGIN_FILE, "w") as f:
        for sid, pwd in logins.items():
            f.write(f"{sid},{pwd}\n")


# ------------------ ADMIN FEATURES ------------------

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            return
        else:
            print("Invalid choice!")


def add_student():
    students = load_students()
    logins = load_logins()

    try:
        sid = int(input("Enter ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    if sid in students:
        print("Student ID already exists.")
        return

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    dept = input("Enter Department: ")

    grade_input = input("Enter Grade: ").strip()

    try:
        grade = float(grade_input)
    except ValueError:
        print("Invalid grade. Please enter a numeric value.")
        return



    students[sid] = {
        "name": name,
        "email": email,
        "phone": phone,
        "department": dept,
        "grade": grade
    }

    password = input("Set initial password: ")

    logins[sid] = password

    save_students(students)
    save_logins(logins)

    print("Student added successfully!")


def view_all_students():
    students = load_students()
    if not students:
        print("No students found.")
        return

    print("\nID | Name | Email | Phone | Department | Grade")
    print("---------------------------------------------------")
    for sid, data in students.items():
        print(f"{sid} | {data['name']} | {data['email']} | {data['phone']} | "
              f"{data['department']} | {data['grade']}")


def update_student():
    students = load_students()

    try:
        sid = int(input("Enter student ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    if sid not in students:
        print("Student ID not found.")
        return

    print("Leave blank to keep old value.")

    name = input(f"New Name ({students[sid]['name']}): ") or students[sid]['name']
    email = input(f"New Email ({students[sid]['email']}): ") or students[sid]['email']
    phone = input(f"New Phone ({students[sid]['phone']}): ") or students[sid]['phone']
    dept = input(f"New Department ({students[sid]['department']}): ") or students[sid]['department']

    grade_input = input(f"New Grade ({students[sid]['grade']}): ")
    grade = float(grade_input) if grade_input else students[sid]['grade']

    students[sid] = {
        "name": name,
        "email": email,
        "phone": phone,
        "department": dept,
        "grade": grade
    }

    save_students(students)
    print("Student updated successfully!")


def delete_student():
    students = load_students()
    logins = load_logins()

    try:
        sid = int(input("Enter student ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    if sid not in students:
        print("Student ID not found.")
        return

    del students[sid]
    logins.pop(sid, None)

    save_students(students)
    save_logins(logins)

    print("Student deleted successfully!")


# ------------------ STUDENT FEATURES ------------------

def student_menu(sid):
    students = load_students()
    while True:
        print(f"\n--- Student Menu ({sid}) ---")
        print("1. View Profile")
        print("2. Edit Personal Info")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            s = students[sid]
            print("\n--- Profile ---")
            print(f"ID: {sid}")
            print(f"Name: {s['name']}")
            print(f"Email: {s['email']}")
            print(f"Phone: {s['phone']}")
            print(f"Department: {s['department']}")
            print(f"Grade: {s['grade']}")

        elif choice == "2":
            s = students[sid]
            print("Leave blank to keep old value.")

            name = input(f"New Name ({s['name']}): ") or s['name']
            email = input(f"New Email ({s['email']}): ") or s['email']
            phone = input(f"New Phone ({s['phone']}): ") or s['phone']
            dept = input(f"New Department ({s['department']}): ") or s['department']

            s.update({
                "name": name,
                "email": email,
                "phone": phone,
                "department": dept
            })

            save_students(students)
            print("Profile updated.")

        elif choice == "3":
            return

        else:
            print("Invalid choice!")


# ------------------ LOGIN SYSTEM ------------------

def admin_login():
    while True:
        print("\n--- Admin Login ---")
        user = input("Username: ")
        password = input("Password: ")

        if user == ADMIN_USER and password == ADMIN_PASS:
            print("Login successful!")
            admin_menu()
            return
        else:
            print("Invalid credentials.")

def student_login():
    logins = load_logins()
    students = load_students()

    while True:
        print("\n--- Student Login ---")
        try:
            sid = int(input("Student ID: "))
        except ValueError:
            print("Invalid ID.")
            continue

        password = input("Password: ")

        if sid in logins and logins[sid] == password:
            print("Login successful!")
            student_menu(sid)
            return
        else:
            print("Invalid credentials.")


# ------------------ MAIN ------------------

def main():
    while True:
        print("\n--- Student Management System ---")
        print("1. Admin Login")
        print("2. Student Login")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            admin_login()
        elif choice == "2":
            student_login()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
