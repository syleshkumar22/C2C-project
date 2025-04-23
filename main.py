
import mysql.connector
import random

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="38@Action",
        database="example"
    )

def generate_account_number():
    return random.randint(1000000000, 9999999999)

def login(cursor):
    name = input("Enter your name: ")
    account = input("Enter your account number: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE name = %s AND account = %s AND password = %s", (name, account, password))
    user = cursor.fetchone()

    if user:
        print(f"\nLogin successful. Welcome, {user[1]}!")
        return user
    else:
        print("Login failed.")
        create = input("Do you want to create a new account? (yes/no): ").lower()
        if create == "yes":
            return create_account(cursor)
        else:
            return None

def create_account(cursor):
    name = input("Enter your full name: ")
    password = input("Set a password: ")
    account_num = generate_account_number()

    cursor.execute("INSERT INTO users (name, account, password, money) VALUES (%s, %s, %s, %s)", (name, account_num, password, 0.0))
    connection.commit()

    cursor.execute("SELECT * FROM users WHERE account = %s", (account_num,))
    user = cursor.fetchone()
    print(f"Account created successfully!\nName: {name}\nAccount Number: {account_num}")
    return user

def show_menu():
    print("\nAvailable actions:")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Close Account")
    print("5. Logout")
    return input("Choose an action (1-5): ")

def get_balance(cursor, user):
    cursor.execute("SELECT money FROM users WHERE id = %s", (user[0],))
    balance = cursor.fetchone()[0] or 0.00
    print(f"Your current balance is: ${balance:.2f}")

def deposit_money(cursor, connection, user):
    amount = input("Enter amount to deposit: ")
    if amount.replace('.', '', 1).isdigit():
        amount = float(amount)
        cursor.execute("UPDATE users SET money = IFNULL(money, 0) + %s WHERE id = %s", (amount, user[0]))
        connection.commit()
        print(f"Deposited ${amount:.2f} successfully.")
    else:
        print("Invalid amount entered.")

def withdraw_money(cursor, connection, user):
    amount = input("Enter amount to withdraw: ")
    if amount.replace('.', '', 1).isdigit():
        amount = float(amount)
        cursor.execute("SELECT money FROM users WHERE id = %s", (user[0],))
        balance = cursor.fetchone()[0] or 0.00
        if amount <= balance:
            cursor.execute("UPDATE users SET money = money - %s WHERE id = %s", (amount, user[0]))
            connection.commit()
            print(f"Withdrew ${amount:.2f} successfully.")
        else:
            print("Insufficient balance.")
    else:
        print("Invalid amount entered.")

def close_account(cursor, connection, user):
    confirm = input("Are you sure you want to close your account? This cannot be undone (yes/no): ").lower()
    if confirm == "yes":
        cursor.execute("DELETE FROM users WHERE id = %s", (user[0],))
        connection.commit()
        print("Your account has been closed and deleted.")
        return True
    else:
        print("Account closure canceled.")
        return False

def main():
    global connection
    connection = connect_db()
    cursor = connection.cursor()

    user = login(cursor)
    if not user:
        return

    while True:
        choice = show_menu()

        if choice == "1":
            get_balance(cursor, user)
        elif choice == "2":
            deposit_money(cursor, connection, user)
        elif choice == "3":
            withdraw_money(cursor, connection, user)
        elif choice == "4":
            if close_account(cursor, connection, user):
                break
        elif choice == "5":
            print("Logging out. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()