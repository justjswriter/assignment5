import json

class RentServ:
    def __init__(self):
        self.goods = []

    def addgoods(self, goods):
        self.goods.append(goods)

    def searchgoods(self, keyword):
        foundgoods = []
        for goods in self.goods:
            if keyword.lower() in goods['name'].lower():
                foundgoods.append(goods)
        return foundgoods

class RentGiver:
    def __init__(self, name):
        self.name = name

class RentSeeker:
    def __init__(self, name):
        self.name = name

def savedata(data):
    with open('goods.json', 'w') as file:
        json.dump(data, file)

def loaddata():
    try:
        with open('goods.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def main():
    service = RentServ()
    service.goods = loaddata()

    while True:
        print("\n1. Add Goods")
        print("2. Search Goods")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name of the goods: ")
            description = input("Enter description: ")
            price = float(input("Enter price: "))
            goods = {'name': name, 'description': description, 'price': price}
            service.addgoods(goods)
            savedata(service.goods)
            print("Goods added successfully!")
        elif choice == '2':
            keyword = input("Enter keyword to search: ")
            found_goods = service.searchgoods(keyword)
            if found_goods:
                print("Found Goods:")
                for goods in found_goods:
                    print(f"Name: {goods['name']}, Description: {goods['description']}, Price: {goods['price']}")
            else:
                print("No goods found matching the keyword.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
