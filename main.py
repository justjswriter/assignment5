import csv
import json

class RentService:
    def __init__(self):
        self.goods = []
        self.users = {}

    def add_goods(self, user_id, name, description, price):
        if user_id not in self.users:
            return "User is not authorized."
        goods = {'name': name, 'description': description, 'price': price}
        self.goods.append(goods)
        self.save_goods_to_csv()
        return "Added successfully."

    def search_goods(self, keyword):
        found_goods = []
        for goods in self.goods:
            if keyword.lower() in goods['name'].lower():
                found_goods.append(goods)
        return found_goods

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        return False

    def register(self, username, password):
        if username in self.users:
            return "User already exists."
        self.users[username] = password
        self.save_users_to_csv()
        return "User registered successfully."

    def load_users_from_csv(self):
        with open('users.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.users[row[0]] = row[1]

    def save_users_to_csv(self):
        with open('users.csv', mode='w') as file:
            writer = csv.writer(file)
            for user, password in self.users.items():
                writer.writerow([user, password])

    def load_goods_from_csv(self):
        with open('goods.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.goods.append(row)

    def save_goods_to_csv(self):
        with open('goods.csv', mode='w', newline='') as file:
            fieldnames = ['name', 'description', 'price']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for goods in self.goods:
                writer.writerow(goods)

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
                while True:
                    print("\n1. Add Goods")
                    print("2. Search Goods")
                    print("3. Logout")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == '1':
                        name = input("Enter name of the goods: ")
                        description = input("Enter description: ")
                        price = float(input("Enter price: "))
                        print(rent_service.add_goods(username, name, description, price))
                    elif sub_choice == '2':
                        keyword = input("Enter keyword to search: ")
                        found_goods = rent_service.search_goods(keyword)
                        if found_goods:
                            print("Found Goods:")
                            for goods in found_goods:
                                print(f"Name: {goods['name']}, Description: {goods['description']}, Price: {goods['price']}")
                        else:
                            print("No goods found matching the keyword.")
                    elif sub_choice == '3':
                        print("Logout successful.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Invalid username or password.")
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(rent_service.register(username, password))
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
