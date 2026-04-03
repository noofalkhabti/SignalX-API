from __future__ import annotations
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

CITY_REGION_MAP = {
    "riyadh": ["الرياض", "Riyadh", "Riyadh Region"],
    "jeddah": ["مكة المكرمة", "Makkah Region", "Makkah", "Jeddah"],
    "dammam": ["المنطقة الشرقية", "Eastern Province", "Eastern Region", "Dammam"],
}

CITY_DEFAULTS = {
    "riyadh": {"trend_score": 86, "market_strength": 78, "vehicle_density": 300, "bike_ratio": 0.60},
    "jeddah": {"trend_score": 79, "market_strength": 70, "vehicle_density": 245, "bike_ratio": 0.58},
    "dammam": {"trend_score": 72, "market_strength": 64, "vehicle_density": 205, "bike_ratio": 0.55},
}

def _safe_read_csv(filename: str) -> pd.DataFrame:
    path = DATA_DIR / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

def _normalize_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().lower()

def _match_city_region(df: pd.DataFrame, city: str) -> pd.DataFrame:
    if df.empty or "region" not in df.columns:
        return pd.DataFrame()
    aliases = [_normalize_text(x) for x in CITY_REGION_MAP.get(city, [])]
    region_series = df["region"].astype(str).str.strip().str.lower()
    mask = False
    for alias in aliases:
        mask = mask | region_series.str.contains(alias, na=False)
    return df[mask].copy()

def _latest_national_demand_signal() -> float:
    daily = _safe_read_csv("khamsat_daily_summary.csv")
    if daily.empty or "project_count" not in daily.columns:
        return 65.0
    daily["project_count"] = pd.to_numeric(daily["project_count"], errors="coerce").fillna(0)
    return float(daily["project_count"].tail(7).mean())

def get_external_signal_summary(city: str) -> dict:
    defaults = CITY_DEFAULTS[city]
    trends = _safe_read_csv("google_trends_regions_clean.csv")
    matched = _match_city_region(trends, city)

    trend_cols = [c for c in matched.columns if c.endswith("_interest")] if not matched.empty else []
    if matched.empty or not trend_cols:
        trend_score = float(defaults["trend_score"])
        market_strength = float(defaults["market_strength"])
    else:
        for col in trend_cols:
            matched[col] = pd.to_numeric(matched[col], errors="coerce").fillna(0)
        trend_score = float(matched[trend_cols].mean(axis=1).mean())
        candidate_cols = [c for c in ["delivery_interest", "khamsat_interest", "mostaql_interest", "bahr_interest"] if c in matched.columns]
        market_strength = float(matched[candidate_cols].mean(axis=1).mean()) if candidate_cols else trend_score

    national_signal = _latest_national_demand_signal()

    estimated_vehicle_density = round(
        (defaults["vehicle_density"] * 0.55)
        + (trend_score * 1.45)
        + (national_signal * 0.75)
    )

    estimate_multiplier = round(
        0.92 + (trend_score / 400.0) + (national_signal / 1000.0),
        3
    )

    return {
        "city": city,
        "trend_score": round(trend_score, 2),
        "market_strength": round(market_strength, 2),
        "national_demand_signal": round(national_signal, 2),
        "estimated_vehicle_density": round(estimated_vehicle_density, 2),
        "bike_ratio": defaults["bike_ratio"],
        "estimate_multiplier": estimate_multiplier,
        "data_dir": str(DATA_DIR)
    }
