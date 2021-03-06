
import datetime
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv() # loads environment variables from the ".env" file

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
SENDGRID_TEMPLATE_ID = os.environ.get("SENDGRID_TEMPLATE_ID", "OOPS, please set env var called 'SENDGRID_TEMPLATE_ID'")
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS", "OOPS, please set env var called 'EMAIL_ADDRESS'")

TAX_RATE = 0.0875

# adapted from: https://github.com/prof-rossetti/nyu-info-2335-201905/blob/master/notes/python/datatypes/numbers.md
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes. \n
    Example: to_usd(4000.444444) \n
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017

timestamp = datetime.datetime.now()
human_friendly_timestamp = timestamp.strftime("%Y-%m-%d %H:%M")

#
# CAPTURE AND VALIDATE USER SELECTIONS
#

selected_products = [] # capturing products instead of ids, so I can pass them straight to the email template later

while True:
    selected_id = input("Please input a product id, or 'DONE': " )

    if selected_id.upper() == "DONE":
        break # (break out of the while loop)
    else:
        try:
            #print("LOOKING UP PRODUCT", selected_id)
            matching_products = [p for p in products if str(p["id"]) == str(selected_id)]
            matching_product = matching_products[0] # this will trigger an IndexError if there are no matching products
            selected_products.append(matching_product)
        except IndexError as e:
            #print(e) #> IndexError: list index out of range
            print("Oh, product not found. Please try again...")
            #next # (next iteration of the while loop)

if not selected_products:
    print("Oh, expecting you to select some products before completing the process. Please try again.")
    exit()

#
# CALCULATE TAX AND TOTALS
#

subtotal = sum([float(p["price"]) for p in selected_products])
tax = subtotal * TAX_RATE
total = subtotal + tax

#
# DISPLAY RECEIPT ON SCREEN
#

print("---------------------------")
print("WELCOME TO THE 'QUIET CAR' GROCERY STORE!")
print("CHECKOUT AT:", human_friendly_timestamp)
print("---------------------------")
print("SELECTED PRODUCTS:")
for p in selected_products:
    print(f"... {p['name']} {to_usd(p['price'])}")

print("---------------------------")
print("SUBTOTAL:", to_usd(subtotal))
print("TAX:", to_usd(tax))
print("TOTAL:", to_usd(total))

#
# SEND RECEIPT VIA SENDGRID "TEMPLATE EMAIL"
# see: https://github.com/prof-rossetti/nyu-info-2335-201905/blob/master/notes/python/packages/sendgrid.md
#

print("Would you like a receipt?")
user_email_address = input("Please input your email address, or 'N' to opt-out: ")

if user_email_address.upper() == "Y":
    print(f"Hello Superuser! Using your default email address {EMAIL_ADDRESS} :-D")
    user_email_address = EMAIL_ADDRESS

if user_email_address.upper() in ["N", "NO", "N/A"]:
    print("You've elected to not receive a receipt via email.")
elif "@" not in user_email_address:
    print("Oh, detected invalid email address.")
else:
    print("Sending receipt via email...")

    # format all product prices as we'd like them to appear in the email...
    formatted_products = []
    for p in selected_products:
        formatted_product = p
        if not isinstance(formatted_product["price"], str): # weird that this is necessary, only when there are duplicative selections, like 1,1 or 1,2,1 or 3,2,1,2 because when looping through and modifying a previous identical dict, it appears Python treats the next identical dict as the same object that we updated, so treating it as a copy of the first rather than its own unique object in its own right.
            formatted_product["price"] = to_usd(p["price"])
        formatted_products.append(formatted_product)

    receipt = {
        "subtotal_price_usd": to_usd(subtotal),
        "tax_price_usd": to_usd(tax),
        "total_price_usd": to_usd(total),
        "human_friendly_timestamp": human_friendly_timestamp,
        "products": formatted_products
    }
    #print(receipt)

    client = SendGridAPIClient(SENDGRID_API_KEY)

    message = Mail(from_email=user_email_address, to_emails=user_email_address)
    message.template_id = SENDGRID_TEMPLATE_ID
    message.dynamic_template_data = receipt

    response = client.send(message)

    if str(response.status_code) == "202":
        print("Email sent successfully!")
    else:
        print("Oh, something went wrong with sending the email.")
        print(response.status_code)
        print(response.body)

print("Thanks for shopping!")
