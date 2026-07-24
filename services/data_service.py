import csv

class DataService:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.airports = {}
        self.airlines = {}
        self.load_data()

    def load_data(self):
        # Load Airports
        try:
            with open(f'{self.data_dir}/airports.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    iata = row['iata'].strip().upper()
                    try:
                        lat = float(row['latitude'])
                        lon = float(row['longitude'])
                        self.airports[iata] = {'lat': lat, 'lon': lon, 'city': row['city'], 'state': row['state']}
                    except ValueError:
                        continue
            print(f"Loaded {len(self.airports)} airports.")
        except Exception as e:
            print(f"Error loading airports: {e}")

        # Load Airlines
        try:
            with open(f'{self.data_dir}/airlines_us_only.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    code = row['Code'].strip()
                    name = row['Description'].strip()
                    self.airlines[code] = name
            # Sort airlines by name
            self.airlines = dict(sorted(self.airlines.items(), key=lambda item: item[1]))
            print(f"Loaded {len(self.airlines)} airlines.")
        except Exception as e:
            print(f"Error loading airlines: {e}")

    def get_airports(self):
        return self.airports

    def get_airlines(self):
        return self.airlines
