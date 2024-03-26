import os
import json

class DhatuKosha:
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(__file__), "dhatu_kosha.json")
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

    def get_dhatu_info(self, dhatu):
        for dhatu_info in self.data.get("Dhatus", []):
            if dhatu_info.get("dhatu") == dhatu:
                return dhatu_info
        return None

    def get_all_dhatus(self):
        return [dhatu_info.get("dhatu") for dhatu_info in self.data.get("Dhatus", [])]

    def get_dhatus_by_gana(self, gana):
        return [dhatu_info for dhatu_info in self.data.get("Dhatus", []) if dhatu_info.get("gana") == gana]

    def get_dhatus_by_lakshana(self, lakshana):
        return [dhatu_info for dhatu_info in self.data.get("Dhatus", []) if dhatu_info.get("lakshana") == lakshana]

    def get_dhatus_by_tense_usage(self, tense, usage):
        return [dhatu_info for dhatu_info in self.data.get("Dhatus", []) if dhatu_info.get("tense_usage", {}).get(tense) == usage]

    def add_dhatu(self, dhatu_info):
        dhatus = self.data.get("Dhatus", [])
        dhatus.append(dhatu_info)
        self.data["Dhatus"] = dhatus
        self.save_data()

    def update_dhatu(self, dhatu, new_dhatu_info):
        dhatus = self.data.get("Dhatus", [])
        for idx, dhatu_info in enumerate(dhatus):
            if dhatu_info.get("dhatu") == dhatu:
                dhatus[idx] = new_dhatu_info
                self.data["Dhatus"] = dhatus
                self.save_data()
                return True
        return False

    def delete_dhatu(self, dhatu):
        dhatus = self.data.get("Dhatus", [])
        for idx, dhatu_info in enumerate(dhatus):
            if dhatu_info.get("dhatu") == dhatu:
                del dhatus[idx]
                self.data["Dhatus"] = dhatus
                self.save_data()
                return True
        return False

    def save_data(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

# Example usage:
if __name__ == "__main__":
    dhatu_kosha = DhatuKosha()

    # Get information for a specific dhatu
    dhatu_info = dhatu_kosha.get_dhatu_info("कृ")
    if dhatu_info:
        print("Dhatu:", dhatu_info.get("dhatu"))
        print("Gana:", dhatu_info.get("gana"))
        print("Lakshana:", dhatu_info.get("lakshana"))
        print("Example Usage:", dhatu_info.get("example_usage"))

    # Get information for all dhatus
    all_dhatus = dhatu_kosha.get_all_dhatus()
    print("All Dhatus:")
    for dhatu in all_dhatus:
        print("-", dhatu)

    # Search dhatus by gana
    gana_dhatus = dhatu_kosha.get_dhatus_by_gana("तिङ्")
    print("Dhatus with Gana 'तिङ्':", [dhatu.get("dhatu") for dhatu in gana_dhatus])

    # Add a new dhatu
    new_dhatu_info = {
        "dhatu": "धा",
        "gana": "आदि",
        "lakshana": "धारणम्",
        "example_usage": "धातवः"
    }
    dhatu_kosha.add_dhatu(new_dhatu_info)

    # Update an existing dhatu
    updated_dhatu_info = {
        "dhatu": "कृ",
        "gana": "तिङ्",
        "lakshana": "कार्य",
        "example_usage": "कर्तुं कारणे, कर्मणि विधिः. Updated example usage."
    }
    dhatu_kosha.update_dhatu("कृ", updated_dhatu_info)

    # Delete a dhatu
    dhatu_kosha.delete_dhatu("धा")
