import unittest

from src.utils import validate_receipt
from src.utils import validate_receipt_items
from src.utils import validate_receipt_total
from src.utils import validate_receipt_retailer
from src.utils import validate_receipt_purchase_date
from src.utils import validate_receipt_purchase_time
from src.utils import validate_receipt_item_properties

class TestValidation(unittest.TestCase):
    def test_receipt_items(self):
        valid_items = [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            {"shortDescription": "Dasani", "price": "1.40"}
        ]
        invalid_item_description = [
            {"shortDescription": "Gummy@Bears", "price": "1.00"}
        ]
        invalid_item_price = [
            {"shortDescription": "Gummy Bears", "price": "1"}
        ]

        self.assertTrue(validate_receipt_items(valid_items))
        self.assertFalse(validate_receipt_items(""))                        # not a list
        self.assertFalse(validate_receipt_items([]))                        # empty list
        self.assertFalse(validate_receipt_items(invalid_item_description))  # invalid item description
        self.assertFalse(validate_receipt_items(invalid_item_price))        # invalid item price

    def test_receipt_items_properties(self):
        valid_items = [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
            {"shortDescription": "Gatorade", "price": "2.25"},
            {"shortDescription": "Dasani", "price": "1.40"},
            {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
            {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
            {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
            {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
            {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
        ]
        invalid_item_description = {"shortDescription": "Gummy@Bears", "price": "1.00"}
        invalid_item_price = {"shortDescription": "Gummy Bears", "price": "1"}
        invalid_item_price_integer = {"shortDescription": "Gummy Bears", "price": 1}
        missing_item_price = {"shortDescription": "Gummy Bears"}
        missing_item_description = {"price": "1.00"}

        for item in valid_items:
            self.assertTrue(validate_receipt_item_properties(item))

        self.assertFalse(validate_receipt_item_properties(""))                          # not a dictionary
        self.assertFalse(validate_receipt_item_properties({}))                          # empty dictionary
        self.assertFalse(validate_receipt_item_properties(invalid_item_description))    # invalid item description
        self.assertFalse(validate_receipt_item_properties(invalid_item_price))          # invalid item price
        self.assertFalse(validate_receipt_item_properties(missing_item_price))          # missing item price
        self.assertFalse(validate_receipt_item_properties(missing_item_description))    # missing item description
        self.assertFalse(validate_receipt_item_properties(invalid_item_price_integer))  # integer item price 

    def test_receipt_retailer(self):
        self.assertTrue(validate_receipt_retailer("7-Eleven"))
        self.assertTrue(validate_receipt_retailer("Target"))
        self.assertFalse(validate_receipt_retailer(7))              # not a str
        self.assertFalse(validate_receipt_retailer(""))             # empty str
        self.assertFalse(validate_receipt_retailer("7@Eleven"))     # invalid character
        
    
    def test_receipt_purchase_date(self):
        self.assertTrue(validate_receipt_purchase_date("2022-03-20"))
        self.assertTrue(validate_receipt_purchase_date("2022-01-02"))
        self.assertTrue(validate_receipt_purchase_date("2018-02-10"))      
        self.assertFalse(validate_receipt_purchase_date(2014))          # not a str
        self.assertFalse(validate_receipt_purchase_date("2014"))        # not a date
        self.assertFalse(validate_receipt_purchase_date("02-08-1998"))  # invalid format
        self.assertFalse(validate_receipt_purchase_date("1090-13-15"))  # no 13th month
        self.assertFalse(validate_receipt_purchase_date("2014-12-32"))  # no 32nd day

    def test_receipt_purchase_time(self):
        self.assertTrue(validate_receipt_purchase_time("08:13"))
        self.assertTrue(validate_receipt_purchase_time("13:01"))
        self.assertTrue(validate_receipt_purchase_time("13:13"))
        self.assertTrue(validate_receipt_purchase_time("14:33"))
        self.assertFalse(validate_receipt_purchase_time(9))         # integer
        self.assertFalse(validate_receipt_purchase_time(":"))       # not a time
        self.assertFalse(validate_receipt_purchase_time("12"))      # invalid format
        self.assertFalse(validate_receipt_purchase_time("28:30"))   # no 28th hour
        self.assertFalse(validate_receipt_purchase_time("23:61"))   # no 61st minute
        self.assertFalse(validate_receipt_purchase_time("234:303")) # invalid time
        
    def test_receipt_total(self):
        self.assertTrue(validate_receipt_total("9.00"))
        self.assertTrue(validate_receipt_total("2.65"))
        self.assertTrue(validate_receipt_total("1.25"))
        self.assertTrue(validate_receipt_total("09.00"))
        self.assertTrue(validate_receipt_total("30.33"))
        self.assertFalse(validate_receipt_total(9))         # integer
        self.assertFalse(validate_receipt_total("9"))       # invalid format
        self.assertFalse(validate_receipt_total("9.999"))   # 999 is not a valid cent
        self.assertFalse(validate_receipt_total("-9.90"))   # negative price

    def test_receipt(self):
        invalid_receipt = {
            "retailer": "7@Eleven",
            "purchaseDate": "2022-13-20",
            "purchaseTime": "28:30",
            "total": "12345",
            "items": [
                {"shortDescription": "Beef#Jerky", "price": "2.25"}
            ]
        }

        corner_receipt = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "total": "9.00",
            "items": [
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"}
            ]
        }

        self.assertTrue(validate_receipt(corner_receipt))
        self.assertFalse(validate_receipt(invalid_receipt))
    
if __name__ == '__main__':
    unittest.main()