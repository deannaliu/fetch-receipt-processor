import re
import math
from datetime import datetime

# Validate the receipt data based on api.yaml
#  - retailer
#  - purchaseDate
#  - purchaseTime
#  - items
#  - total
def validate_receipt(receipt_data):
    receipt_schema = {"retailer", "purchaseDate", "purchaseTime", "items", "total"}
    
    for field in receipt_schema:
        if field not in receipt_data:
            return False
        
    valid_retailer = validate_receipt_retailer(receipt_data["retailer"])
    valid_purchase_date = validate_receipt_purchase_date(receipt_data["purchaseDate"])
    valid_purchase_time = validate_receipt_purchase_time(receipt_data["purchaseTime"])
    valid_items = validate_receipt_items(receipt_data["items"])
    valid_total = validate_receipt_total(receipt_data["total"])

    if not valid_retailer or not valid_purchase_date or not valid_purchase_time or not valid_items or not valid_total:
        return False
    return True

# Validate receipt retailer data based on api.yaml
# "^[\w\s\-&]+$"
def validate_receipt_retailer(retailer):
    if not re.match(r"^[\w\s\-&]+$", retailer):
        return False
    return True

# Validate receipt retailer data based on api.yaml
# "YYYY-MM-DD" & Valid Date
def validate_receipt_purchase_date(purchase_date):
    try:
        datetime.strptime(purchase_date, "%Y-%m-%d")
    except ValueError:
        return False
    return True

# Validate receipt retailer data based on api.yaml
# "HH:MM" 24Hr
def validate_receipt_purchase_time(purchase_time):
    try:
        datetime.strptime(purchase_time, "%H:%M")
    except ValueError:
        return False
    return True

# Validate receipt retailer data based on api.yaml
# valid list & not empty
# example list item: {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
def validate_receipt_items(items):
    if not isinstance(items, list) or len(items) < 1:
        return False
    return True

# Validate receipt retailer data based on api.yaml
# "^\d+\.\d{2}$"
def validate_receipt_total(total):
    if not re.match(r"^\d+\.\d{2}$", total):
        return False
    return True


# Calculate Points for Receipt
def calculate_points(receipt_data):
    points = 0

    # 1 point for every alphanumeric character in the retailer name
    points += calculate_points_retailer(receipt_data["retailer"])
    # points generated from receipt total dollar amount
    points += calculate_points_total_amount(receipt_data["total"])
    # 5 points for every two items on the receipt
    points += calculate_points_items_amount(receipt_data["items"])
    # points generated from receipt item description
    points += calculate_points_item_description(receipt_data["items"])
    # 6 points if the day in the purchase date is odd
    points += calculate_points_purchase_date(receipt_data["purchaseDate"])
    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    points += calculate_points_purchase_time(receipt_data["purchaseTime"])

    return points

def calculate_points_retailer(retailer):
    return sum(c.isalnum() for c in retailer)

def calculate_points_total_amount(total):
    points = 0
    
    # 50 points if the total is a round dollar amount (e.g., 10.00)
    if re.match(r"^\d+\.00$", total):
        points += 50
    
    # 25 points if the total is a multiple of 0.25 (e.g., 7.25)
    if float(total) % 0.25 == 0:
        points += 25
    
    return points

def calculate_points_items_amount(items):
    return (len(items) // 2) * 5

def calculate_points_item_description(items):
    # if the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. 
    points = 0

    for item in items:
        if len(item['shortDescription'].strip()) % 3 == 0:
            points += math.ceil(float(item['price']) * 0.2)
    return points

def calculate_points_purchase_date(purchase_date):
    # checking if the purchase date is odd
    try: 
        day = datetime.strptime(purchase_date, "%Y-%m-%d").day
        if day % 2 != 0:
            return 6
    except ValueError:
        pass
    return 0

def calculate_points_purchase_time(purchase_time):
    # checking if the purchase time is between 2-4pm
    try:
        time = datetime.strptime(purchase_time, "%H:%M").time()
        if 14 <= time.hour < 16:
            return 10
    except ValueError:
        pass
    return 0