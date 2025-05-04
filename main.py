import matplotlib.pyplot as plt
from sqlQuery import access_table
from apiQuery import get_sightmap_data
import numpy as np

def process_info():
    sql_data = None
    expense_data = None
    highest_price = {}
    lowest_price = {}
    all_rent_dict = {}
    sql_dict = {}
    api_dict = {}
    floor_plans = []
    avg_rent = []
    building_amount = {}

    sql_data = access_table()
    API_Data = get_sightmap_data()
    unit_data = API_Data['units']
    expense_data = API_Data['expenses']
    required_fees = 0
    mon_pet_rent = 0
    init_rent_pet = 0

    for fee in expense_data:
        label_key = fee['label']
        frequency_key = fee['frequency']
        if label_key == 'Initial Pet Fee':
            init_rent_pet += float(fee['amount'])
        elif label_key == 'Pet Premium':
            mon_pet_rent += float(fee['amount'])
            init_rent_pet += float(fee['amount'])
        elif label_key == 'Storage':
            key_list = list(highest_price.keys())
            for element in key_list:
                highPrice = highest_price[element]
                highest_price[element + ' With Minimum Storage'] = highPrice + float(fee['min_amount'])
                highest_price[element + ' With Maximum Storage'] = highPrice + float(fee['max_amount'])
        if frequency_key == 'monthly' and fee['is_required']:
            required_fees += float(fee['amount'])

    for item in sql_data:
        floor_plan_key = item['floor_plan']
        if floor_plan_key in sql_dict:
            temp_dict = sql_dict[floor_plan_key]
            temp_dict['price'] = item['unit_price'] + temp_dict['price']
            temp_list = all_rent_dict[floor_plan_key]
            temp_list.append(item['unit_price'] + required_fees)
            all_rent_dict[floor_plan_key] = temp_list
            temp_dict['amount'] = 1 + temp_dict['amount']
            sql_dict[floor_plan_key] = temp_dict
            if highest_price[floor_plan_key] < item['unit_price']:
                highest_price[floor_plan_key] = item['unit_price']
            elif lowest_price[floor_plan_key] > item['unit_price']:
                lowest_price[floor_plan_key] = item['unit_price']
            
        else:
            sql_dict[floor_plan_key] = {'price': item['unit_price'], 'amount': 1}
            all_rent_dict[floor_plan_key] = [item['unit_price']]
            lowest_price[floor_plan_key] = item['unit_price']
            highest_price[floor_plan_key] = item['unit_price']
            floor_plans.append(floor_plan_key)   

    for unit in unit_data:
        unit_floor_plan = unit['floor_plan_id']
        if unit_floor_plan in api_dict:
            temp_dict_2 = api_dict[unit_floor_plan]
            temp_dict_2['area'] = unit['area'] + temp_dict_2['area']
            temp_dict_2['amount'] = 1 + temp_dict_2['amount']
            api_dict[unit_floor_plan] = temp_dict_2
        else:
            api_dict[unit_floor_plan] = {'area': unit['area'], 'amount' : 1}
        if unit['building_id'] in building_amount:
            building_amount[unit['building_id']] += 1
        else:
            building_amount[unit['building_id']] = 1
        
    print(building_amount)

    for rent in sql_dict:
        temp_dict = sql_dict[rent]
        rent_value = round((temp_dict['price'] / temp_dict['amount']), 2) + required_fees
        avg_rent.append(rent_value)
        print('\nTotal Amount of ' + str(rent) + " units is " + str(temp_dict['amount']))
    floor_plan_index = 0
    for area in api_dict:
        temp_dict_2 = api_dict[area]
        area_value = round((temp_dict_2['area'] / temp_dict_2['amount']), 2)
        print("\nAverage sq ft. of " + floor_plans[floor_plan_index] + " is: " + str(area_value))
        price_per_sqFt = round((avg_rent[floor_plan_index] / area_value), 2)
        print("\nAverage price per sq. foot of " + floor_plans[floor_plan_index] + " units is " + str(price_per_sqFt))
        floor_plan_index += 1

    init_rent_pet += avg_rent[0]
    mon_pet_rent += avg_rent[0]

    print("\nAverage First Month's Rent with Pet for S1 floor plans: " + str(round(init_rent_pet, 2)))
    print("\nAverage Monthly Rent with Pet for S1 floor plans: " + str(round(mon_pet_rent, 2)))

    highest_list = list(highest_price.values())
    highest_total = max(highest_list) + required_fees + 200
    lowest_list = list(lowest_price.values())
    lowest_total = min(lowest_list)
    for avg in floor_plans:
        print("\nAverage Price of " + avg + " is: " + str(avg_rent[floor_plans.index(avg)]))
    for lp in lowest_price:
        print("\nLowest Price of " + lp + " is: " + str(lowest_price[lp] + required_fees))
    for hp in highest_price:
        print("\nHighest Price of " + hp + " is: " + str(highest_price[hp] + required_fees))   
             
    x_values = []
    y_values = []

    
    for i, plan in enumerate(floor_plans):
        rents = all_rent_dict.get(plan, [])
        x_values.extend([i + np.random.uniform(-0.1, 0.1) for _ in rents])  # Slightly offset x for clarity
        y_values.extend(rents)

    plt.figure(figsize=(8, 5))
    plt.scatter(x_values, y_values, color='blue', marker='o', alpha=0.7, label="Individual Prices")
    plt.scatter(floor_plans, avg_rent, color='red', marker='o', alpha=0.9, label="Average Price")
    plt.ylim(lowest_total, highest_total)
    plt.xlabel("Floor Plan Type")
    plt.ylabel("Average Rent ($)")
    plt.title("Average Rent vs Floor Plans")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.show()

def main():
    process_info()

if __name__ == "__main__":
    main()