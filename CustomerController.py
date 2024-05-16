from UserInputError import UserInputError
from CustomerInterface import CustomerInterface
# from RowNotFoundError import RowNotFoundError
from domain.Customer import Customer
from domain.ShoppingCart import ShoppingCart
import csv


class CustomerController():
    def __init__(self, inventory):
        # super().__init__()
        self.ui = CustomerInterface()
        self.customer = Customer(inventory)

        
    def __check_input(self, input):
        if len(input) == 0:
            raise UserInputError

    def add_to_cart(self, product):
        self.customer.add_to_cart(product)

    def view_shopping_cart(self):
        self.customer.view_shopping_cart()
        self.cart_operation_displat()
        select = input("Please input your option:\n")
        if select=='1':
            order_list = []
            product_name = input("Please input the product name:\n")
            delivery_way = input("Please input the delivery way(eg:delivery or pickup):\n")
            for index,item in enumerate(self.customer.shopping_cart.items):
                if item['product'].name==product_name:
                    self.customer.shopping_cart.items.pop(index)
                    order_list.append([item["product"].id,item["product"].name,item["product"].brand,item["product"].og_price,item["quantity"],delivery_way])
            if len(order_list)>0:
                with open('db/order.txt','a') as f:
                    f.write("id,name,brand,og_price,quantity,delivery\n")
                    for item in order_list:
                        f.write(",".join([str(value) for value in item])+"\n")
                print("Pay finish!")
            else:
                print("There is no product")
        else:
            pass

    def cart_operation_displat(self):
        print("\nCheck out\n [1]Pay for a product\n [2]Quiz")



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
                    # case "3":
                    #     self.view_shopping_cart()
                    #     display_menu = True
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
                        self.add_to_cart(product)
                    case "2":
                        self.view_shopping_cart()
                    case "q":
                        return
                    case _:
                        raise UserInputError
            except UserInputError as e:
                print("Invalid input.")

    def pay_product(self,):
        pass