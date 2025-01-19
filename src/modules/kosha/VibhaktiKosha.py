import os
import json

class VibhaktiKosha:
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(__file__), "VibhaktiKosha.json")
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
        except Exception as e:
            print(f"Error saving data: {e}")

    def validate_vibhakti_info(self, vibhakti_info):
        required_keys = ["noun", "vibhaktis"]
        for key in required_keys:
            if key not in vibhakti_info:
                raise ValueError(f"Missing required key: {key}")
        return True

    def get_vibhakti_info(self, noun):
        for vibhakti_info in self.data.get("Nouns", []):
            if vibhakti_info.get("noun") == noun:
                return vibhakti_info
        return None

    def get_all_nouns(self):
        return [vibhakti_info.get("noun") for vibhakti_info in self.data.get("Nouns", [])]

    def get_vibhaktis_by_case(self, case):
        return [vibhakti_info for vibhakti_info in self.data.get("Nouns", []) if case in vibhakti_info.get("vibhaktis", {})]

    def add_vibhakti(self, vibhakti_info):
        self.validate_vibhakti_info(vibhakti_info)
        if self.get_vibhakti_info(vibhakti_info["noun"]):
            raise ValueError(f"Noun '{vibhakti_info['noun']}' already exists.")
        self.data.setdefault("Nouns", []).append(vibhakti_info)
        self.save_data()

    def update_vibhakti(self, noun, new_vibhakti_info):
        self.validate_vibhakti_info(new_vibhakti_info)
        nouns = self.data.get("Nouns", [])
        for idx, vibhakti_info in enumerate(nouns):
            if vibhakti_info.get("noun") == noun:
                nouns[idx] = new_vibhakti_info
                self.data["Nouns"] = nouns
                self.save_data()
                return True
        return False

    def delete_vibhakti(self, noun):
        nouns = self.data.get("Nouns", [])
        for idx, vibhakti_info in enumerate(nouns):
            if vibhakti_info.get("noun") == noun:
                del nouns[idx]
                self.data["Nouns"] = nouns
                self.save_data()
                return True
        return False

    def search_vibhaktis(self, **criteria):
        results = self.data.get("Nouns", [])
        for key, value in criteria.items():
            results = [vibhakti_info for vibhakti_info in results if vibhakti_info.get(key) == value]
        return results

    def count_nouns(self):
        return len(self.data.get("Nouns", []))

    def list_unique_vibhaktis(self):
        unique_vibhaktis = set()
        for vibhakti_info in self.data.get("Nouns", []):
            unique_vibhaktis.update(vibhakti_info.get("vibhaktis", {}).keys())
        return list(unique_vibhaktis)

# Example usage:
if __name__ == "__main__":
    vibhakti_kosha = VibhaktiKosha()

    # Get information for a specific noun
    vibhakti_info = vibhakti_kosha.get_vibhakti_info("राम")
    if vibhakti_info:
        print("Noun:", vibhakti_info.get("noun"))
        print("Vibhaktis:", vibhakti_info.get("vibhaktis"))

    # Get information for all nouns
    all_nouns = vibhakti_kosha.get_all_nouns()
    print("All Nouns:")
    for noun in all_nouns:
        print("-", noun)

    # Search vibhaktis by case
    case_vibhaktis = vibhakti_kosha.get_vibhaktis_by_case("प्रथमा")
    print("Nouns with Prathama Vibhakti:")
    for vibhakti in case_vibhaktis:
        print("-", vibhakti.get("noun"))

    # Add a new vibhakti
    new_vibhakti_info = {
        "noun": "गणेश",
        "vibhaktis": {
            "प्रथमा": "गणेशः",
            "द्वितीया": "गणेशम्",
            "तृतीया": "गणेशेन",
            "चतुर्थी": "गणेशाय",
            "पञ्चमी": "गणेशात्",
            "षष्ठी": "गणेशस्य",
            "सप्तमी": "गणेशे",
            "सम्बोधन": "गणेश"
        }
    }
    vibhakti_kosha.add_vibhakti(new_vibhakti_info)

    # Update an existing vibhakti
    updated_vibhakti_info = {
        "noun": "राम",
        "vibhaktis": {
            "प्रथमा": "रामः",
            "द्वितीया": "रामम्",
            "तृतीया": "रामेण",
            "चतुर्थी": "रामाय",
            "पञ्चमी": "रामात्",
            "षष्ठी": "रामस्य",
            "सप्तमी": "रामे",
            "सम्बोधन": "राम"
        }
    }
    vibhakti_kosha.update_vibhakti("राम", updated_vibhakti_info)

    # Delete a vibhakti
    vibhakti_kosha.delete_vibhakti("गणेश")

    # Search vibhaktis by multiple criteria
    search_results = vibhakti_kosha.search_vibhaktis(noun="राम")
    print("Search Results:", search_results)

    # Count the number of nouns
    print("Total Nouns:", vibhakti_kosha.count_nouns())

    # List all unique vibhaktis
    print("Unique Vibhaktis:", vibhakti_kosha.list_unique_vibhaktis())
