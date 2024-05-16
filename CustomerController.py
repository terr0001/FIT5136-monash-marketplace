from UserInputError import UserInputError
from CustomerInterface import CustomerInterface
# from RowNotFoundError import RowNotFoundError
from domain.Customer import Customer
import csv


class CustomerController():
    def __init__(self, inventory):
        # super().__init__()
        self.ui = CustomerInterface()
        self.customer = Customer(inventory)
        
    def __check_input(self, input):
        if len(input) == 0:
            raise UserInputError
        
    def view_shopping_cart(self):
        # TODO: implement shopping cart
        pass
    
    def add_to_cart(self):
        cart_add = input("Add to Cart (please enter the product ID number of the product you wish to add to cart): ")
        with open('db/product.txt', 'r+', newline='') as f2:
            with open('db/cart.txt', 'a', newline='') as w2:
                reader = csv.reader(f2, delimiter=',')
                for row in reader:
                    if row and row[0] == cart_add:  # Code inspired from Author: wwii, Link: https://stackoverflow.com/questions/39336449/python-check-if-value-in-csv-file
                        w2.write(str(row))
                        w2.write('\n')
                        print("You have successfully added ", row)
                    else:
                        print("That item is not in stock or is not selling")

    def customer_control(self):
        quit_flag = False
        display_menu = True
        while not quit_flag:
            if display_menu:
                self.ui.display_home()

            inp = input().strip().lower()

            try:
                self.__check_input(inp)


                match inp:
                    case "1":
                        self.browse_all_products()
                        display_menu = True
                    case "2":
                        self.view_shopping_cart()
                        display_menu = True
                    case "q":
                        return
                    case _:
                        display_menu = False
                        raise UserInputError
            except UserInputError as e:
                print(
                    "Invalid input. Please enter 1, 2 to perform an action or 'q' to quit.")

    def browse_all_products(self):
        quit_flag = False

        while not quit_flag:
            options = []
            products = self.customer.get_all_products()
            options = self.ui.display_product_list(products)

            inp = input().strip().lower()

            try:
                self.__check_input(inp)
                if inp == "q":
                    return

                inp_found = False
                for op in options:
                    if inp == str(op[0]):
                        self.product_detail(op[1])
                        inp_found = True
                        break

                if not inp_found:
                    raise UserInputError

            except UserInputError as e:
                self.ui.display_result_msg("Invalid input.")

    def product_detail(self, product):
        quit_flag = False

        while not quit_flag:
            self.ui.display_product_details(product)
            
            inp = input().strip().lower()

            try:
                self.__check_input(inp)
                match inp:
                    case "1":
                        self.add_to_cart()
                    case "2":
                        self.view_shopping_cart()
                    case "q":
                        return
                    case _:
                        raise UserInputError
            except UserInputError as e:
                print("Invalid input.")
