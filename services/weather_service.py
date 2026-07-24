import csv

class WeatherService:
    def __init__(self, data_path='data/origin_month_weather_medians.csv'):
        self.data_path = data_path
        self.weather_medians = {}
        self.load_weather_data()

    def load_weather_data(self):
        self.weather_medians = {}
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # CSV columns: Origin,Month,origin_temp_c,origin_dewpt_c,origin_slp_hpa,origin_wind_ms,origin_precip_mm
                    origin = row['Origin'].strip()
                    try:
                        month = int(row['Month'])
                        vals = {
                            "origin_temp_c": float(row['origin_temp_c']),
                            "origin_dewpt_c": float(row['origin_dewpt_c']),
                            "origin_slp_hpa": float(row['origin_slp_hpa']),
                            "origin_wind_ms": float(row['origin_wind_ms']),
                            "origin_precip_mm": float(row['origin_precip_mm'])
                        }
                        self.weather_medians[(origin, month)] = vals
                    except ValueError:
                        continue # Skip bad rows
            print(f"Loaded weather medians for {len(self.weather_medians)} (origin, month) pairs.")
        except Exception as e:
            print(f"Error loading weather medians: {e}")
            self.weather_medians = {}

    def get_weather(self, origin, month):
        # Default weather values
        weather_defaults = {
            "origin_temp_c": 15.0,
            "origin_dewpt_c": 10.0,
            "origin_slp_hpa": 1015.0,
            "origin_wind_ms": 4.0,
            "origin_precip_mm": 0.0
        }
        return self.weather_medians.get((origin, month), weather_defaults)
