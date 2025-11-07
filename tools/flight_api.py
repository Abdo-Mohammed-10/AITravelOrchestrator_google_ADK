import random
from datetime import datetime, timedelta
from typing import List, Dict

# Small in-memory mock database of carriers and sample routes
_CARRIERS = [
    "Air France", "Singapore Airlines", "Qatar Airways",
    "Emirates", "Turkish Airlines", "KLM", "Lufthansa"
]

# Example mock routes (IATA pairs -> approximate base price multiplier)
_ROUTE_BASE = {
    ("JFK", "DPS"): 800,
    ("JFK", "LHR"): 400,
    ("LAX", "NRT"): 700,
    ("CDG", "DPS"): 600,
    ("DXB", "DPS"): 300,
    ("BOM", "DPS"): 150
}

def _fmt_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")

def _generate_flight_number(carrier_name: str) -> str:
    # e.g. "AF6753" -> take uppercase initials and random digits
    initials = "".join([w[0] for w in carrier_name.split()][:2]).upper()
    return f"{initials}{random.randint(100, 9999)}"

def _sample_routes(origin: str, destination: str, date: str, limit: int = 3) -> List[Dict]:
    # Determine a base price from known routes or fallback to random base
    base = _ROUTE_BASE.get((origin, destination), _ROUTE_BASE.get((destination, origin), 400))
    flights = []
    try:
        # if date provided try parse, else pick tomorrow
        if date:
            # accept YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
            dt = datetime.fromisoformat(date) if "T" in date else datetime.fromisoformat(date + "T08:00:00")
        else:
            dt = datetime.utcnow() + timedelta(days=1)
    except Exception:
        dt = datetime.utcnow() + timedelta(days=1)

    for i in range(limit):
        dep_offset_hours = random.randint(1, 48)
        arr_offset_hours = dep_offset_hours + random.randint(8, 18)
        dep_time = dt + timedelta(hours=dep_offset_hours)
        arr_time = dt + timedelta(hours=arr_offset_hours)

        carrier = random.choice(_CARRIERS)
        price_variation = random.uniform(0.85, 1.4)
        price = int(base * price_variation + random.randint(-50, 120))

        flights.append({
            "airline": carrier,
            "flight_number": _generate_flight_number(carrier),
            "departure_iata": origin,
            "arrival_iata": destination,
            "departure_time": _fmt_dt(dep_time),
            "arrival_time": _fmt_dt(arr_time),
            "duration_hours": round((arr_time - dep_time).total_seconds() / 3600, 1),
            "stops": random.choice([0, 1, 2]),
            "price_usd": price,
            "booking_url": f"https://mockbookings.example.com/{origin}-{destination}/{random.randint(10000,99999)}"
        })
    # sort by price ascending
    flights.sort(key=lambda x: x["price_usd"])
    return flights

def search_flights(departure_iata: str, arrival_iata: str, date: str = "") -> dict:
    """
    Mock search_flights tool for testing ADK flight agent.
    Args:
        departure_iata (str): origin airport IATA (e.g., 'JFK')
        arrival_iata (str): destination airport IATA (e.g., 'DPS')
        date (str): optional travel date 'YYYY-MM-DD' or ISO 'YYYY-MM-DDTHH:MM:SS'
    Returns:
        dict: {"status": "success", "result": {...}} or {"status":"error", "error": "..."}
    """
    departure_iata = (departure_iata or "").upper()
    arrival_iata = (arrival_iata or "").upper()
    if not departure_iata or not arrival_iata:
        return {"status": "error", "error": "departure_iata and arrival_iata are required strings."}

    try:
        flights = _sample_routes(departure_iata, arrival_iata, date, limit=4)
        # Provide a "cheapest" summary and a small list
        if not flights:
            return {"status": "error", "error": "No mock flights found."}

        cheapest = flights[0]
        return {
            "status": "success",
            "result": {
                "origin": departure_iata,
                "destination": arrival_iata,
                "requested_date": date or "",
                "cheapest": cheapest,
                "offers": flights
            }
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
