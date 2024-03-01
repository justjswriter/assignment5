import csv
import json

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Goods:
    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

class RentService:
    def __init__(self):
        self.users = {}
        self.goods = []

    def add_user(self, username, password):
        if username in self.users:
            return "User already exists."
        self.users[username] = password
        self.save_users_to_csv()
        return "User registered successfully."

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        return False

    def add_goods(self, user, name, description, price):
        if user.username not in self.users:
            return "User is not authorized."
        goods = Goods(name, description, price)
        self.goods.append(goods)
        self.save_goods_to_csv()
        return "Goods added successfully."

    def search_goods(self, keyword):
        found_goods = []
        for goods in self.goods:
            if keyword.lower() in goods.name.lower():
                found_goods.append(goods)
        return found_goods

    def delete_goods(self, user, name):
        if user.username not in self.users:
            return "User is not authorized."

        found = False
        for i, goods in enumerate(self.goods):
            if goods.name.lower() == name.lower():
                del self.goods[i]
                found = True
                break

        if found:
            self.save_goods_to_csv()
            return "Goods deleted successfully."
        else:
            return "Goods not found."

    def update_goods(self, user, name, new_description, new_price):
        if user.username not in self.users:
            return "User is not authorized."

        for goods in self.goods:
            if goods.name.lower() == name.lower():
                goods.description = new_description
                goods.price = new_price
                self.save_goods_to_csv()
                return "Goods information updated successfully."

        return "Goods not found."

    def view_all_goods(self):
        return self.goods

    def change_password(self, username, old_password, new_password):
        if username in self.users and self.users[username] == old_password:
            self.users[username] = new_password
            self.save_users_to_csv()
            return "Password changed successfully."
        else:
            return "Invalid username or password."

    def view_user_profile(self, username):
        if username in self.users:
            return f"Username: {username}"
        else:
            return "User not found."

    def load_users_from_csv(self):
        try:
            with open('users.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.users[row[0]] = row[1]
        except FileNotFoundError:
            pass

    def save_users_to_csv(self):
        with open('users.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for user, password in self.users.items():
                writer.writerow([user, password])

    def load_goods_from_csv(self):
        try:
            with open('goods.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    goods = Goods(row['name'], row['description'], float(row['price']))
                    self.goods.append(goods)
        except FileNotFoundError:
            pass

    def save_goods_to_csv(self):
        with open('goods.csv', mode='w', newline='') as file:
            fieldnames = ['name', 'description', 'price']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for goods in self.goods:
                writer.writerow({'name': goods.name, 'description': goods.description, 'price': goods.price})

def main():
    rent_service = RentService()
    rent_service.load_users_from_csv()
    rent_service.load_goods_from_csv()

    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if rent_service.login(username, password):
                print("Login successful.")
                user = User(username, password)
                while True:
                    print("\n1. Add Goods")
                    print("2. Search Goods")
                    print("3. Delete Goods")
                    print("4. Update Goods Information")
                    print("5. View All Goods")
                    print("6. Change Password")
                    print("7. View User Profile")
                    print("8. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == '1':
                        name = input("Enter name of the goods: ")
                        description = input("Enter description: ")
                        price = float(input("Enter price: "))
                        print(rent_service.add_goods(user, name, description, price))
                    elif sub_choice == '2':
                        keyword = input("Enter keyword to search: ")
                        found_goods = rent_service.search_goods(keyword)
                        if found_goods:
                            print("Found Goods:")
                            for goods in found_goods:
                                print(f"Name: {goods.name}, Description: {goods.description}, Price: {goods.price}")
                        else:
                            print("No goods found matching the keyword.")
                    elif sub_choice == '3':
                        name = input("Enter name of the goods to delete: ")
                        print(rent_service.delete_goods(user, name))
                    elif sub_choice == '4':
                        name = input("Enter name of the goods to update: ")
                        new_description = input("Enter new description: ")
                        new_price = float(input("Enter new price: "))
                        print(rent_service.update_goods(user, name, new_description, new_price))
                    elif sub_choice == '5':
                        all_goods = rent_service.view_all_goods()
                        print("All Goods:")
                        for goods in all_goods:
                            print(f"Name: {goods.name}, Description: {goods.description}, Price: {goods.price}")
                    elif sub_choice == '6':
                        old_password = input("Enter current password: ")
                        new_password = input("Enter new password: ")
                        print(rent_service.change_password(username, old_password, new_password))
                    elif sub_choice == '7':
                        print(rent_service.view_user_profile(username))
                    elif sub_choice == '8':
                        print("Logout successful.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid username or password.")
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(rent_service.add_user(username, password))
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
