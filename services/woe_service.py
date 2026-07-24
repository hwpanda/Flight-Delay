import json

class WOEService:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.airline_woe = {}
        self.origin_woe = {}
        self.dest_woe = {}
        self.global_woe = 0.0
        self.load_woe_maps()

    def load_woe_maps(self):
        try:
            with open(f'{self.data_dir}/airline_woe.json', 'r', encoding='utf-8') as f:
                self.airline_woe = json.load(f)
            with open(f'{self.data_dir}/origin_woe.json', 'r', encoding='utf-8') as f:
                self.origin_woe = json.load(f)
            with open(f'{self.data_dir}/dest_woe.json', 'r', encoding='utf-8') as f:
                self.dest_woe = json.load(f)
            with open(f'{self.data_dir}/global_woe.json', 'r', encoding='utf-8') as f:
                self.global_woe = json.load(f).get("global_woe", 0.0)

            print(
                f"Loaded WOE maps: {len(self.airline_woe)} airlines, "
                f"{len(self.origin_woe)} origins, {len(self.dest_woe)} destinations. "
                f"GLOBAL_WOE={self.global_woe:.4f}"
            )
        except Exception as e:
            print(f"Error loading WOE maps: {e}")
            self.airline_woe, self.origin_woe, self.dest_woe = {}, {}, {}
            self.global_woe = 0.0

    def get_woe(self, airline, origin, dest):
        return {
            "airline_woe": self.airline_woe.get(airline, self.global_woe),
            "origin_woe": self.origin_woe.get(origin, self.global_woe),
            "dest_woe": self.dest_woe.get(dest, self.global_woe)
        }
