import csv
from domain import Product
from domain import Category
from domain import SubCategory
from RowNotFoundError import RowNotFoundError


class DbHelper:
    db_path = "db"
    CATEGORY_TBL_FILE_NAME = "category.txt"
    CUSTOMER_TBL_FILE_NAME = "customer.txt"
    FOODPRODUCT_TBL_FILE_NAME = "foodproduct.txt"
    PRODUCT_TBL_FILE_NAME = "product.txt"
    SUBCATEGORY_TBL_FILE_NAME = "subcategory.txt"
    USER_TBL_FILE_NAME = "user.txt"

    @classmethod
    def __get_data(self, filename):
        with open(f"{self.db_path}/{filename}", mode="r", encoding="UTF-8") as f:
            data = list(csv.DictReader(f, delimiter=','))
            return data

    @classmethod
    def get_all_products(self):
        product_dict_list = self.__get_data(self.PRODUCT_TBL_FILE_NAME)
        products = []

        for product_dict in product_dict_list:
            product = Product.Product(
                product_dict['product_id'],
                product_dict['product_name'],
                product_dict['product_brand'],
                product_dict['product_desc'],
                product_dict['product_qty'],
                product_dict['product_og_price'],
                product_dict['product_member_price'],
                product_dict['subcat_id']
            )
            products.append(product)

        return products

    # @classmethod
    # def __get_all_subcategories(self, category_id_index_map):

    @classmethod
    def get_all_categories(self):
        cat_dict_list = self.__get_data(self.CATEGORY_TBL_FILE_NAME)
        subcat_dict_list = self.__get_data(self.SUBCATEGORY_TBL_FILE_NAME)
        subcategories = []
        categories = []
        cat_id_index_map = [None] * (int(cat_dict_list[-1]['cat_id']) + 1)

        for i, dict in enumerate(cat_dict_list):
            cat_id = int(dict['cat_id'])

            category = Category.Category(
                cat_id,
                dict['cat_name']
            )
            # id, name
            cat_id_index_map[cat_id] = i
            categories.append(category)

        for dict in subcat_dict_list:
            subcategory = SubCategory.SubCategory(
                int(dict['subcat_id']),
                dict['subcat_name']
            )

            category = categories[cat_id_index_map[int(dict['cat_id'])]] 
            category.add_subcategory(subcategory)
            subcategories.append(subcategory)
            
        return (categories, subcategories)

    @classmethod
    def get_all_foodproduct(self):
        return self.__get_data(self.FOODPRODUCT_TBL_FILE_NAME)

    @classmethod
    def __get_new_id(self, file):
        *_, last_row = csv.reader(file, delimiter=',')
        new_id = int(last_row[0]) + 1
        return new_id

    @classmethod
    def add_product(self, name, brand, description, quantity, sub_category_id, og_price, member_price):
        with open(f"{self.db_path}/{self.PRODUCT_TBL_FILE_NAME}", 'r+', newline="") as f:
            product_id = self.__get_new_id(f)
            product = Product.Product(
                product_id, name, brand, description, quantity, sub_category_id, og_price, member_price)

            writer = csv.writer(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([product_id, name, product.brand, description,
                            quantity, sub_category_id, og_price, member_price])

            return product

    @classmethod
    def delete_product(self, product_id):
        deleted = False
        prod_list = []
        with open(f"{self.db_path}/{self.PRODUCT_TBL_FILE_NAME}", 'r+', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            # lines = f.readlines()
            for line in reader:
                if line[0] != str(product_id):
                    prod_list.append(line)
                    # f.write(line)
                else:
                    deleted = True

            f.seek(0)
            writer = csv.writer(
                f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(prod_list)

            f.truncate()

        if not deleted:
            raise RowNotFoundError

    @classmethod
    def update_product(self, product_id, name=None, brand=None, description=None, quantity=None, sub_category_id=None,
                       og_price=None, member_price=None):
        # 读取原始数据
        data = self.__get_data(self.PRODUCT_TBL_FILE_NAME)

        # 找到要更新的产品在数据中的索引
        index = None
        for i, row in enumerate(data):
            print("这个是：", row['product_id'])
            if row['product_id'] == product_id:
                index = i
                break

        print("是否成功复制", index)

        # 如果找到了产品
        if index is not None:
            # 更新产品信息
            if name is not None:
                data[index]['product_name'] = name
            if brand is not None:
                data[index]['product_brand'] = brand
            if description is not None:
                data[index]['product_desc'] = description
            if quantity is not None:
                data[index]['product_qty'] = quantity
            if sub_category_id is not None:
                data[index]['subcat_id'] = sub_category_id
            if og_price is not None:
                data[index]['product_og_price'] = og_price
            if member_price is not None:
                data[index]['product_member_price'] = member_price

            # 写入更新后的数据到文件
            with open(f"{self.db_path}/{self.PRODUCT_TBL_FILE_NAME}", mode="w", newline='', encoding="UTF-8") as f:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(data)

            print("Product updated successfully.")
        else:
            print(f"Product with ID {product_id} not found.")


if __name__ == "__main__":
    db = DbHelper()
    # p = Product.Product(7, "name", "brand", "description", 10, 6.9, 5, 11)
    db.get_all_categories()
    # db.add_product("Colgate Total Charcoal Deep Clean Toothpaste", "Colgate",
    #    "Colgate Total Antibacterial Fluoride toothpaste has a unique formula that keeps your whole mouth healthy by fighting bacteria on teeth, tongue, cheeks, and gums for 12 hours*. Colgate Total Charcoal Deep Clean, active cleaning formula fights plaque even between teeth and hard to reach spaces", 10, 6.9, 5, 11)
