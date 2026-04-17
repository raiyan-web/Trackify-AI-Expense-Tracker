"""
Generate 100 rows of simulated Uber ride data for the
Ride Cancellation & Customer Satisfaction analytics project.
"""

import random
import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

random.seed(42)

# --- Reference lists ---
cities = ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Chennai"]

locations = {
    "Bangalore": ["Koramangala", "Whitefield", "Indiranagar", "MG Road", "Electronic City",
                  "Hebbal", "Airport", "Jayanagar", "Marathahalli", "BTM Layout"],
    "Mumbai":    ["Andheri", "Bandra", "Powai", "Dadar", "Airport", "Juhu",
                  "Lower Parel", "Worli", "Thane", "Navi Mumbai"],
    "Delhi":     ["Connaught Place", "Saket", "Dwarka", "Airport", "Nehru Place",
                  "Lajpat Nagar", "Karol Bagh", "Rohini", "Noida", "Gurgaon"],
    "Hyderabad": ["Hitech City", "Gachibowli", "Banjara Hills", "Secunderabad", "Airport",
                  "Ameerpet", "Kukatpally", "Madhapur", "LB Nagar", "Jubilee Hills"],
    "Chennai":   ["T Nagar", "Anna Nagar", "Adyar", "OMR", "Airport",
                  "Velachery", "Tambaram", "Guindy", "Nungambakkam", "Mylapore"],
}

ride_categories = ["UberGo", "UberPool", "UberPremier", "UberXL"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Wallet"]
weather_conditions = ["Clear", "Cloudy", "Rainy", "Foggy"]
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

cancellation_reasons_customer = [
    "Driver too far", "Found alternate transport", "Fare too high",
    "Changed plans", "Booked by mistake", "Long wait time",
    "Driver asked to cancel", "Wrong pickup location entered"
]
cancellation_reasons_driver = [
    "Customer unreachable", "Wrong address", "Too much traffic",
    "Customer asked to cancel", "Route not preferred", "Vehicle issue"
]

# --- Helper functions ---
def random_timestamp():
    start = datetime.datetime(2025, 1, 1)
    end = datetime.datetime(2025, 12, 31)
    delta = end - start
    rand_days = random.randint(0, delta.days)
    rand_secs = random.randint(0, 86399)
    return start + datetime.timedelta(days=rand_days, seconds=rand_secs)

def generate_row(i):
    city = random.choice(cities)
    city_locs = locations[city]
    pickup = random.choice(city_locs)
    dropoff = random.choice([l for l in city_locs if l != pickup])

    booking_ts = random_timestamp()
    hour = booking_ts.hour
    day = days_of_week[booking_ts.weekday()]
    is_peak = hour in [8, 9, 17, 18, 19]
    is_weekend = day in ["Saturday", "Sunday"]

    ride_cat = random.choices(ride_categories, weights=[50, 25, 15, 10])[0]
    surge = round(random.choices(
        [1.0, round(random.uniform(1.1, 1.5), 1), round(random.uniform(1.6, 2.0), 1),
         round(random.uniform(2.1, 3.0), 1)],
        weights=[50, 25, 15, 10]
    )[0], 1)

    est_wait = random.randint(2, 15)
    driver_rating = round(random.uniform(3.0, 5.0), 1)
    customer_rating = round(random.uniform(3.5, 5.0), 1)
    distance = round(random.uniform(1.5, 30.0), 1)
    base_fare = round(distance * random.uniform(8, 14) * surge, 2)
    weather = random.choices(weather_conditions, weights=[50, 25, 15, 10])[0]
    payment = random.choice(payment_methods)
    is_repeat = random.choices([True, False], weights=[65, 35])[0]

    # Determine ride status with weighted probabilities
    cancel_weight = 0
    cancel_weight += max(0, (est_wait - 5) * 3)        # long wait → more cancel
    cancel_weight += max(0, (surge - 1.0) * 20)         # high surge → more cancel
    cancel_weight += max(0, (4.0 - driver_rating) * 15) # low rating → more cancel
    if weather == "Rainy":
        cancel_weight += 10
    if is_peak:
        cancel_weight += 5

    cancel_prob = min(cancel_weight / 100, 0.60)
    is_cancelled = random.random() < cancel_prob

    if is_cancelled:
        who = random.choices(["Cancelled_Customer", "Cancelled_Driver"], weights=[70, 30])[0]
        ride_status = who
        if who == "Cancelled_Customer":
            cancel_reason = random.choice(cancellation_reasons_customer)
        else:
            cancel_reason = random.choice(cancellation_reasons_driver)
        actual_wait = random.randint(est_wait, est_wait + 10)
        cancel_time_sec = random.randint(30, 600)
        csat = ""
        driver_id = f"DRV-{random.randint(1000,9999)}" if random.random() > 0.2 else ""
    else:
        no_driver_chance = 0.05
        if random.random() < no_driver_chance:
            ride_status = "No_Driver"
            cancel_reason = "No driver available"
            actual_wait = ""
            cancel_time_sec = ""
            csat = ""
            driver_id = ""
        else:
            ride_status = "Completed"
            cancel_reason = ""
            actual_wait = random.randint(max(1, est_wait - 3), est_wait + 5)
            cancel_time_sec = ""
            csat = random.choices([5, 4, 3, 2, 1], weights=[35, 35, 15, 10, 5])[0]
            driver_id = f"DRV-{random.randint(1000,9999)}"

    booking_id = f"BK-{booking_ts.strftime('%Y%m%d')}-{i:03d}"
    customer_id = f"CUST-{random.randint(1000, 5000)}"

    return [
        booking_id, customer_id, driver_id,
        booking_ts.strftime("%Y-%m-%d %H:%M:%S"),
        pickup, dropoff,
        round(random.uniform(12.8, 28.7), 4),   # pickup_lat
        round(random.uniform(72.8, 80.3), 4),    # pickup_lng
        ride_cat, est_wait, actual_wait,
        round(base_fare, 2), surge,
        driver_rating, customer_rating,
        ride_status, cancel_reason, cancel_time_sec,
        distance, payment, csat,
        is_repeat, day, hour, weather, city
    ]

# --- Generate CSV ---
headers = [
    "booking_id", "customer_id", "driver_id", "booking_timestamp",
    "pickup_location", "dropoff_location", "pickup_lat", "pickup_lng",
    "ride_category", "estimated_wait_time", "actual_wait_time",
    "estimated_fare", "surge_multiplier", "driver_rating", "customer_rating",
    "ride_status", "cancellation_reason", "cancellation_time_sec",
    "trip_distance_km", "payment_method", "customer_satisfaction",
    "is_repeat_customer", "day_of_week", "hour_of_day", "weather_condition", "city"
]

rows = [generate_row(i) for i in range(1, 101)]

output_path = r"c:\Users\ADMIN\New folder\uber_rides_data.xlsx"

wb = Workbook()
ws = wb.active
ws.title = "Rides Data"

# --- Write header row ---
ws.append(headers)

# Style the header row
header_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
header_fill = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
thin_border = Border(
    bottom=Side(style="thin", color="AAAAAA")
)
for col_idx, cell in enumerate(ws[1], 1):
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

# --- Write data rows ---
for row in rows:
    ws.append(row)

# --- Auto-fit column widths ---
for col in ws.columns:
    max_len = 0
    col_letter = col[0].column_letter
    for cell in col:
        try:
            cell_len = len(str(cell.value)) if cell.value is not None else 0
            if cell_len > max_len:
                max_len = cell_len
        except Exception:
            pass
    ws.column_dimensions[col_letter].width = min(max_len + 3, 30)

# Freeze header row
ws.freeze_panes = "A2"

# Auto-filter
ws.auto_filter.ref = ws.dimensions

# --- Add a Summary sheet ---
ws2 = wb.create_sheet(title="Summary")
ws2.append(["Metric", "Value"])
for cell in ws2[1]:
    cell.font = header_font
    cell.fill = PatternFill(start_color="548235", end_color="548235", fill_type="solid")
    cell.alignment = Alignment(horizontal="center")

statuses = {}
for r in rows:
    s = r[15]
    statuses[s] = statuses.get(s, 0) + 1

ws2.append(["Total Rides", len(rows)])
for status, count in sorted(statuses.items(), key=lambda x: -x[1]):
    ws2.append([status, count])
ws2.append(["Cancellation Rate (%)", round(sum(v for k, v in statuses.items() if "Cancel" in k) / len(rows) * 100, 1)])

ws2.column_dimensions["A"].width = 25
ws2.column_dimensions["B"].width = 15

# Save
wb.save(output_path)
print(f"Generated 100 rows -> {output_path}")
print("\nRide Status Summary:")
for status, count in sorted(statuses.items(), key=lambda x: -x[1]):
    print(f"   {status}: {count}")
