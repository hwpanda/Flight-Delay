import math
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from services.data_service import DataService
from services.model_service import ModelService
from services.weather_service import WeatherService
from services.woe_service import WOEService

app = Flask(__name__)

# Initialize Services
data_service = DataService()
model_service = ModelService()
weather_service = WeatherService()
woe_service = WOEService()

# --- Helper ---

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 3958.8 # Radius of Earth in miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- API Routes ---

@app.route("/")
def index():
    return render_template("index.html", airlines=data_service.get_airlines())

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    print(f"frontend data: {data}")

    flight_date_str = data.get("flight_date")
    dep_time_str = data.get("dep_time")
    arr_time_str = data.get("arr_time")
    airline = data.get("airline")
    origin = data.get("origin")
    dest = data.get("destination")

    # Validate Inputs
    if not all([flight_date_str, dep_time_str, arr_time_str, airline, origin, dest]):
        return jsonify({"error": "Missing required fields"}), 400

    airports = data_service.get_airports()
    if origin not in airports or dest not in airports:
        return jsonify({"error": "Invalid airport code"}), 400

    # Feature 
    try:
        dt = datetime.strptime(flight_date_str, "%Y-%m-%d")
        month = dt.month
        day_of_month = dt.day
        day_of_week = dt.weekday() + 1 # Monday=1, Sunday=7 
        quarter = (month - 1) // 3 + 1
        year = dt.year

        # Time calculations
        # Input format "HH:MM" -> Model format HHMM (int)
        dep_h, dep_m = map(int, dep_time_str.split(':'))
        arr_h, arr_m = map(int, arr_time_str.split(':'))
        
        crs_dep_time = dep_h * 100 + dep_m
        crs_arr_time = arr_h * 100 + arr_m
        
        # Calculate elapsed time in minutes
        dep_minutes = dep_h * 60 + dep_m
        arr_minutes = arr_h * 60 + arr_m
        
        if arr_minutes < dep_minutes:
            # Overnight flight, arrival is next day
            arr_minutes += 24 * 60
            
        crs_elapsed_time = arr_minutes - dep_minutes

    except ValueError:
        return jsonify({"error": "Invalid date or time format"}), 400

    origin_coords = airports[origin]
    dest_coords = airports[dest]
    distance = haversine_distance(origin_coords['lat'], origin_coords['lon'], dest_coords['lat'], dest_coords['lon'])

    # --- WOE lookups ---
    woe_vals = woe_service.get_woe(airline, origin, dest)

    # --- Weather Medians Lookup ---
    weather_vals = weather_service.get_weather(origin, month)
    print(f"Using weather for {origin} in month {month}: {weather_vals}")

    # --- origin_rain ---
    # Map UI input to model features, 
    # TODO: might need to delete this for the new model
    # origin_rain_input = data.get("origin_rain", "missing")
    
    # if origin_rain_input == "0":
    #     origin_rain_missing = 0
    #     origin_rain_num = 0.0
    # elif origin_rain_input == "1":
    #     origin_rain_missing = 0
    #     origin_rain_num = 1.0
    # else:
    #     # Default / Missing
    #     origin_rain_missing = 1
    #     origin_rain_num = -1.0

    # print(f"origin_rain_input: {origin_rain_input} and origin_rain_missing: {origin_rain_missing}")

    # Dummy values for missing data
    features = {
        "Year": year,
        "Quarter": quarter,
        "Month": month,
        "DayofMonth": day_of_month,
        "DayOfWeek": day_of_week,
        "CRSDepTime": crs_dep_time,
        "CRSArrTime": crs_arr_time,
        "CRSElapsedTime": crs_elapsed_time,
        "Distance": distance,
        
        # Weather features from lookup
        "origin_temp_c": weather_vals["origin_temp_c"],
        "origin_dewpt_c": weather_vals["origin_dewpt_c"],
        "origin_slp_hpa": weather_vals["origin_slp_hpa"],
        "origin_precip_mm": weather_vals["origin_precip_mm"],

        "NUMBER_OF_SEATS": 150,
        # WOE dummies
        "Reporting_Airline_woe": woe_vals["airline_woe"],
        "Origin_woe": woe_vals["origin_woe"],
        "Dest_woe": woe_vals["dest_woe"],
    }

    # Prediction
    probability, delayed = model_service.predict(features)
    
    message = "Flight is likely to be delayed." if delayed else "Flight is likely to be on time."
    
    return jsonify({
        "delayed": delayed,
        "probability": probability,
        "message": message,
        "features": features,
        "route": {
            "origin_coords": [origin_coords['lat'], origin_coords['lon']],
            "dest_coords": [dest_coords['lat'], dest_coords['lon']]
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
