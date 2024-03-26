import os
import json

class PratyayaKosha:
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(__file__), "pratyaya_kosha.json")
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: File not found at {self.filepath}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.filepath}")
            return {}

    def get_pratyaya_info(self, pratyaya):
        for pratyaya_info in self.data.get("Pratyayas", []):
            if pratyaya_info.get("pratyaya") == pratyaya:
                return pratyaya_info
        return None

    def get_all_pratyayas(self):
        return self.data.get("Pratyayas", [])

    def search_pratyayas_by_vibhakti(self, vibhakti):
        return [pratyaya_info for pratyaya_info in self.data.get("Pratyayas", []) if pratyaya_info.get("vibhakti") == vibhakti]

    def search_pratyayas_by_gana(self, gana):
        return [pratyaya_info for pratyaya_info in self.data.get("Pratyayas", []) if pratyaya_info.get("gana") == gana]

    def get_pratyayas_by_example(self, example):
        return [pratyaya_info for pratyaya_info in self.data.get("Pratyayas", []) if pratyaya_info.get("example_usage") == example]

# Example usage:
if __name__ == "__main__":
    pratyaya_kosha = PratyayaKosha()

    # Get information for a specific pratyaya
    pratyaya_info = pratyaya_kosha.get_pratyaya_info("ण्")
    if pratyaya_info:
        print("Pratyaya:", pratyaya_info.get("pratyaya"))
        print("Gana:", pratyaya_info.get("gana"))
        print("Vibhakti:", pratyaya_info.get("vibhakti"))
        print("Meaning:", pratyaya_info.get("meaning"))
        print("Example Usage:", pratyaya_info.get("example_usage"))

    # Get information for all pratyayas
    all_pratyayas = pratyaya_kosha.get_all_pratyayas()
    print("All Pratyayas:")
    for pratyaya in all_pratyayas:
        print("-", pratyaya.get("pratyaya"))

    # Search pratyayas by vibhakti
    pratyayas_by_vibhakti = pratyaya_kosha.search_pratyayas_by_vibhakti("तृतीया")
    print("Pratyayas in Tṛtīyā Vibhakti:")
    for pratyaya in pratyayas_by_vibhakti:
        print("-", pratyaya.get("pratyaya"))

    # Search pratyayas by gana
    pratyayas_by_gana = pratyaya_kosha.search_pratyayas_by_gana("तिङ्")
    print("Pratyayas in Tṅ Gana:")
    for pratyaya in pratyayas_by_gana:
        print("-", pratyaya.get("pratyaya"))

    # Get pratyayas by example usage
    pratyayas_by_example = pratyaya_kosha.get_pratyayas_by_example("गङ्गातः")
    print("Pratyayas with Example Usage 'गङ्गातः':")
    for pratyaya in pratyayas_by_example:
        print("-", pratyaya.get("pratyaya"))
