import os
import json

class SamyuktaKosha:
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(__file__), "samyukta_kosha.json")
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

    def save_data(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            print(f"Error: File not found at {self.filepath}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.filepath}")

    def get_samyukta_info(self, samyukta):
        for samyukta_info in self.data.get("Samyuktas", []):
            if samyukta_info.get("samyukta") == samyukta:
                return samyukta_info
        return None

    def get_all_samyuktas(self):
        return [samyukta_info.get("samyukta") for samyukta_info in self.data.get("Samyuktas", [])]

    def search_samyuktas_by_definition(self, keyword):
        return [samyukta_info for samyukta_info in self.data.get("Samyuktas", []) if keyword in samyukta_info.get("definition", "")]

    def search_samyuktas_by_example(self, keyword):
        matching_samyuktas = []
        for samyukta_info in self.data.get("Samyuktas", []):
            examples = samyukta_info.get("examples", [])
            for example in examples:
                if keyword in example:
                    matching_samyuktas.append(samyukta_info)
                    break
        return matching_samyuktas

    def add_samyukta(self, samyukta_info):
        self.data.setdefault("Samyuktas", []).append(samyukta_info)
        self.save_data()

# Example usage:
if __name__ == "__main__":
    samyukta_kosha = SamyuktaKosha()

    # Get information for a specific samyukta
    samyukta_info = samyukta_kosha.get_samyukta_info("संयुक्त")
    if samyukta_info:
        print("Samyukta:", samyukta_info.get("samyukta"))
        print("Definition:", samyukta_info.get("definition"))
        print("Examples:")
        for example in samyukta_info.get("examples", []):
            print("-", example)

    # Get information for all samyuktas
    all_samyuktas = samyukta_kosha.get_all_samyuktas()
    print("All Samyuktas:")
    for samyukta in all_samyuktas:
        print("-", samyukta)

    # Search samyuktas by keyword in definition
    keyword = "विशेष"
    matching_samyuktas = samyukta_kosha.search_samyuktas_by_definition(keyword)
    print(f"Samyuktas with '{keyword}' in definition:")
    for samyukta_info in matching_samyuktas:
        print("-", samyukta_info.get("samyukta"))

    # Search samyuktas by keyword in examples
    keyword = "केन्द्र"
    matching_samyuktas = samyukta_kosha.search_samyuktas_by_example(keyword)
    print(f"Samyuktas with '{keyword}' in examples:")
    for samyukta_info in matching_samyuktas:
        print("-", samyukta_info.get("samyukta"))

    # Add a new samyukta
    new_samyukta = {
        "samyukta": "संयोजित",
        "definition": "एकत्र आधे का आधा",
        "examples": [
            "संयोजित संख्या",
            "संयोजित अंगुल"
        ]
    }
    samyukta_kosha.add_samyukta(new_samyukta)
    print("New samyukta added successfully.")
