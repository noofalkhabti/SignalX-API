from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import APP_NAME, APP_VERSION, ALLOWED_CITIES, OFFICIAL_WORKERS_BASE
from app.services.trends_service import get_trends_features
from app.services.iot_service import get_iot_features, get_live_vehicle_markers
from app.services.feature_service import build_feature_table
from app.services.privacy_service import build_privacy_summary
from app.services.data_service import get_external_signal_summary
from app.models.clustering import run_kmeans
from app.models.regression import run_regression_estimation
from app.models.classification import run_classification
from app.models.weighted_estimation import weighted_estimate

app = FastAPI(title=APP_NAME, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": f"{APP_NAME} is running"}

@app.get("/api/dashboard")
def dashboard(city: str = "riyadh"):
    city = city.strip().lower()
    if city not in ALLOWED_CITIES:
        raise HTTPException(status_code=400, detail=f"Invalid city: {city}")

    trends = get_trends_features(city)
    iot = get_iot_features(city)
    external = get_external_signal_summary(city)

    # Enhance model inputs with uploaded data signals
    trends["trend_score"] = round((trends["trend_score"] * 0.55) + (external["trend_score"] * 0.45), 2)
    trends["store_density"] = round((trends["store_density"] * 0.65) + (external["market_strength"] * 0.35), 2)

    iot["vehicles_live"] = max(
        80,
        round((iot["vehicles_live"] * 0.55) + (external["estimated_vehicle_density"] * 0.45))
    )
    iot["motorcycles_live"] = round(iot["vehicles_live"] * external["bike_ratio"])
    iot["cars_live"] = iot["vehicles_live"] - iot["motorcycles_live"]
    iot["iot_score"] = round(
        (iot["vehicles_live"] * 0.72)
        + (external["national_demand_signal"] * 0.18)
        + (external["trend_score"] * 0.10),
        2
    )

    df = build_feature_table(trends, iot, city)
    df = run_kmeans(df)

    regression = run_regression_estimation(df)
    classification = run_classification(df)

    estimated = weighted_estimate(
        trends["trend_score"],
        iot["iot_score"],
        trends["store_density"],
        iot["time_factor"]
    )

    estimated = round(estimated * external["estimate_multiplier"])
    gap = round(((estimated - OFFICIAL_WORKERS_BASE) / OFFICIAL_WORKERS_BASE) * 100, 1)

    return {
        "city": city,
        "estimated_workers": estimated,
        "official_workers": OFFICIAL_WORKERS_BASE,
        "gap_percent": gap,
        "vehicles_live": iot["vehicles_live"],
        "cars_live": iot["cars_live"],
        "motorcycles_live": iot["motorcycles_live"],
        "peak_window": iot["peak_window"],
        "zones": regression["zones"],
        "clusters": classification["zone_clusters"],
        "privacy": build_privacy_summary(),
        "external_signals": external
    }

@app.get("/api/live-map")
def live_map(city: str = "riyadh"):
    city = city.strip().lower()
    if city not in ALLOWED_CITIES:
        raise HTTPException(status_code=400, detail=f"Invalid city: {city}")
    external = get_external_signal_summary(city)
    return {"vehicles": get_live_vehicle_markers(city, external)}
