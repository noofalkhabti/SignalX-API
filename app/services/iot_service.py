import random
from datetime import datetime
from typing import Optional  # ✅ إضافة مهمة

CITY_CENTERS = {
    "riyadh": (24.7136, 46.6753),
    "jeddah": (21.5433, 39.1728),
    "dammam": (26.4207, 50.0888),
}

APP_BRANDS = ["Jahez", "HungerStation", "ToYou", "Mrsool"]
STORE_BRANDS = ["Danube", "Carrefour", "Panda"]

SOURCES_APP = [
    "Google Trends + Mobility Signals",
    "Aggregated App Demand Pulse",
    "Search Index + Zone Activity"
]

SOURCES_STORE = [
    "Retail Dispatch Pattern",
    "Store Density + Time Factor",
    "Area Activity Aggregation"
]

def get_iot_features(city: str) -> dict:
    hour = datetime.now().hour

    if 11 <= hour <= 14:
        time_factor = 0.85
        peak_window = "12–2 PM"
    elif 18 <= hour <= 21:
        time_factor = 1.00
        peak_window = "6–9 PM"
    else:
        time_factor = 0.60
        peak_window = "Off-Peak"

    vehicles_live = random.randint(180, 320)
    motorcycles_live = int(vehicles_live * 0.58)
    cars_live = vehicles_live - motorcycles_live

    iot_score = round((vehicles_live * 0.7) + (motorcycles_live * 0.3), 2)

    return {
        "vehicles_live": vehicles_live,
        "motorcycles_live": motorcycles_live,
        "cars_live": cars_live,
        "iot_score": iot_score,
        "time_factor": time_factor,
        "peak_window": peak_window
    }

def random_offset(scale=0.05):
    return random.uniform(-scale, scale)

# ✅ هنا كان الخطأ وتم إصلاحه
def get_live_vehicle_markers(city: str, external: Optional[dict] = None) -> list:
    center = CITY_CENTERS.get(city, CITY_CENTERS["riyadh"])
    vehicles = []

    target_count = 24
    if external:
        target_count = max(18, min(70, int(external.get("estimated_vehicle_density", 240) / 6)))

    bike_ratio = external.get("bike_ratio", 0.58) if external else 0.58

    for i in range(target_count):
        operator_type = random.choice(["app", "store"])
        vehicle_type = "motorcycle" if random.random() < bike_ratio else "car"
        movable = random.choice([True, True, True, False])

        if operator_type == "app":
            brand = random.choice(APP_BRANDS)
            source = random.choice(SOURCES_APP)
        else:
            brand = random.choice(STORE_BRANDS)
            source = random.choice(SOURCES_STORE)

        status = random.choice([
            "نشطة الآن",
            "في طريقها للتسليم",
            "في طريقها للاستلام",
            "متوقفة مؤقتًا"
        ])

        lat = center[0] + random_offset(0.09 if city == "riyadh" else 0.07)
        lng = center[1] + random_offset(0.09 if city == "riyadh" else 0.07)

        vehicles.append({
            "id": i + 1,
            "lat": round(lat, 6),
            "lng": round(lng, 6),
            "operator_type": operator_type,
            "vehicle_type": vehicle_type,
            "brand": brand,
            "source": source,
            "status": status,
            "movable": movable
        })

    return vehicles
