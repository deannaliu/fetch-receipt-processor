import re
import datetime

# Validate the receipt data based on api.yaml
#  - retailer
#  - purchaseDate
#  - purchaseTime
#  - items
#  - total
def validate_receipt(data):
    receipt_schema = {"retailer", "purchaseDate", "purchaseTime", "items", "total"}
    
    for field in receipt_schema:
        if field not in data:
            return False
        
    valid_retailer = validate_receipt_retailer(data["retailer"])
    valid_purchase_date = validate_receipt_purchase_date(data["purchaseDate"])
    valid_purchase_time = validate_receipt_purchase_time(data["purchaseTime"])
    valid_items = validate_receipt_items(data["items"])
    valid_total = validate_receipt_total(data["total"])

    if not valid_retailer or not valid_purchase_date or not valid_purchase_time or not valid_items or not valid_total:
        return False
    return True

# Validate receipt retailer data based on api.yaml
# "^[\\w\\s\\-&]+$"
def validate_receipt_retailer(retailer):
    if not re.match(r"^[\\w\\s\\-&]+$", retailer):
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
def validate_receipt_items(items):
    if not isinstance(items, list) or len(items) < 1:
        return False
    return True

# Validate receipt retailer data based on api.yaml
# "^\\d+\\.\\d{2}$"
def validate_receipt_total(total):
    if not re.match(r"^\\d+\\.\\d{2}$", total):
        return False
    return True