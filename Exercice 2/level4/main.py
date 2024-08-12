import json
from datetime import datetime

# Function to calculate the number of days between two dates
def calculate_days_rented(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return (end - start).days + 1

# Function to calculate the adjusted price per day based on the number of days
def calculate_adjusted_price_per_day(base_price_per_day, days_rented):
    total_price = 0
    for day in range(1, days_rented + 1):
        if day > 10:
            daily_price = base_price_per_day * 0.5
        elif day > 4:
            daily_price = base_price_per_day * 0.7
        elif day > 1:
            daily_price = base_price_per_day * 0.9
        else:
            daily_price = base_price_per_day
        total_price += daily_price
    return total_price

# Function to calculate the commission based on the price and days rented
def calculate_commission(price, days_rented):
    total_commission = price * 0.3
    insurance_fee = total_commission * 0.5
    assistance_fee = days_rented * 100  # 100€ par jour
    drivy_fee = total_commission - insurance_fee - assistance_fee
    return {
        "insurance_fee": int(insurance_fee),
        "assistance_fee": int(assistance_fee),
        "drivy_fee": int(drivy_fee)
    }

# Function to calculate the actions for each rental
def calculate_actions(price, commission):
    owner_share = price * 0.7
    return [
        {"who": "driver", "type": "debit", "amount": int(price)},
        {"who": "owner", "type": "credit", "amount": int(owner_share)},
        {"who": "insurance", "type": "credit", "amount": commission["insurance_fee"]},
        {"who": "assistance", "type": "credit", "amount": commission["assistance_fee"]},
        {"who": "drivy", "type": "credit", "amount": commission["drivy_fee"]}
    ]

filename_output = 'data/output.json'
filename_input = 'data/input.json'

# Read the input JSON file
with open(filename_input) as f:
    data = json.load(f)
    
cars = data['cars']
rentals = data['rentals']

results = []

for rental in rentals:
    car_id = rental['car_id']
    car = cars[car_id - 1]
    days_rented = calculate_days_rented(rental['start_date'], rental['end_date'])
    # Calculate the total price with adjusted daily rates
    price_per_day = calculate_adjusted_price_per_day(car['price_per_day'], days_rented)
    price = price_per_day + car['price_per_km'] * rental['distance']
    
    # Calculate the commission
    commission = calculate_commission(price, days_rented)
    
    # Calculate the actions
    actions = calculate_actions(price, commission)
    
    results.append({
        'id': rental['id'],
        'actions': actions
    })

final_result = {'rentals': results}

# Write the result to the output JSON file
with open(filename_output, 'w') as f:
    json.dump(final_result, f, indent=2)

print("Les résultats ont été écrits dans", filename_output)

