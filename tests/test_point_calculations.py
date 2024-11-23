import unittest
import math

from src.utils import calculate_points
from src.utils import calculate_points_retailer
from src.utils import calculate_points_total_amount
from src.utils import calculate_points_items_amount
from src.utils import calculate_points_purchase_time
from src.utils import calculate_points_purchase_date
from src.utils import calculate_points_item_description

class TestPoints(unittest.TestCase):
    # One point for every alphanumeric character in the retailer name.
    # 50 points if the total is a round dollar amount with no cents.
    # 25 points if the total is a multiple of 0.25.
    # 5 points for every two items on the receipt.
    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    # 6 points if the day in the purchase date is odd.
    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.

    def test_points_morning_receipt(self):
        morning_receipt = {
            "retailer": "Walgreens",
            "total": "2.65",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"}
            ],
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13"
        }
        
        self.assertEqual(calculate_points_retailer(morning_receipt["retailer"]), 9)
        self.assertEqual(calculate_points_purchase_date(morning_receipt["purchaseDate"]), 0)
        self.assertEqual(calculate_points_purchase_time(morning_receipt["purchaseTime"]), 0)
        self.assertEqual(calculate_points_total_amount(morning_receipt["total"]), 0)
        self.assertEqual(calculate_points_items_amount(morning_receipt["items"]), 5)
        self.assertEqual(calculate_points_item_description(morning_receipt["items"]), math.ceil(1.25 * 0.2))
        self.assertEqual(calculate_points(morning_receipt), 15)

    def test_points_simple_receipt(self):
        morning_receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }
        
        self.assertEqual(calculate_points_retailer(morning_receipt["retailer"]), 6)
        self.assertEqual(calculate_points_purchase_date(morning_receipt["purchaseDate"]), 0)
        self.assertEqual(calculate_points_purchase_time(morning_receipt["purchaseTime"]), 0)
        self.assertEqual(calculate_points_total_amount(morning_receipt["total"]), 25)
        self.assertEqual(calculate_points_items_amount(morning_receipt["items"]), 0)
        self.assertEqual(calculate_points_item_description(morning_receipt["items"]), 0)
        self.assertEqual(calculate_points(morning_receipt), 31)

    def test_points_target_receipt(self):
        target_receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "total": "35.35",
            "items": [
                {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                {"shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ", "price": "12.00"}
            ]
        }
        
        self.assertEqual(calculate_points_retailer(target_receipt["retailer"]), 6)
        self.assertEqual(calculate_points_purchase_date(target_receipt["purchaseDate"]), 6)
        self.assertEqual(calculate_points_purchase_time(target_receipt["purchaseTime"]), 0)
        self.assertEqual(calculate_points_total_amount(target_receipt["total"]), 0)
        self.assertEqual(calculate_points_items_amount(target_receipt["items"]), 10)
        self.assertEqual(calculate_points_item_description(target_receipt["items"]), 6)
        self.assertEqual(calculate_points(target_receipt), 28)

    def test_points_corner_market_receipt(self):
        corner_market_receipt = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "total": "9.00",
            "items": [
                { "shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"},
                {"shortDescription": "Gatorade", "price": "2.25"}
            ]
        }
            
        self.assertEqual(calculate_points_retailer(corner_market_receipt["retailer"]), 14)
        self.assertEqual(calculate_points_purchase_date(corner_market_receipt["purchaseDate"]), 0)
        self.assertEqual(calculate_points_purchase_time(corner_market_receipt["purchaseTime"]), 10)
        self.assertEqual(calculate_points_total_amount(corner_market_receipt["total"]), 25 + 50)
        self.assertEqual(calculate_points_items_amount(corner_market_receipt["items"]), 10)
        self.assertEqual(calculate_points_item_description(corner_market_receipt["items"]), 0)
        self.assertEqual(calculate_points(corner_market_receipt), 109)

if __name__ == '__main__':
    unittest.main()