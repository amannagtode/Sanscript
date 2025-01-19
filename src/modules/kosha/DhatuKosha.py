import os
import json
import logging
from jsonschema import validate, ValidationError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DhatuKosha:
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(__file__), "DhatuKosha.json")
        self.schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "DhatuKosha",
            "type": "object",
            "properties": {
                "Dhatus": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "dhatu": { "type": "string" },
                            "gana": { "type": "string" },
                            "lakshana": { "type": "string" },
                            "example_usage": { "type": "string" },
                            "meaning": { "type": "string" },
                            "tense_usage": {
                                "type": "object",
                                "properties": {
                                    "present": { "type": "string" },
                                    "past": { "type": "string" },
                                    "future": { "type": "string" }
                                },
                                "required": ["present", "past", "future"]
                            }
                        },
                        "required": ["dhatu", "gana", "lakshana", "example_usage", "meaning", "tense_usage"]
                    }
                }
            },
            "required": ["Dhatus"]
        }
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                validate(instance=data, schema=self.schema)
                return data
        except FileNotFoundError:
            logger.error(f"Error: File not found at {self.filepath}")
            return {}
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {self.filepath}")
            return {}
        except ValidationError as e:
            logger.error(f"JSON validation error: {e.message}")
            return {}
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return {}

    def save_data(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving data: {e}")

    def validate_dhatu_info(self, dhatu_info):
        required_keys = ["dhatu", "gana", "lakshana", "example_usage", "meaning", "tense_usage"]
        for key in required_keys:
            if key not in dhatu_info:
                raise ValueError(f"Missing required key: {key}")
        return True

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

    def add_dhatu(self, dhatu_info):
        self.validate_dhatu_info(dhatu_info)
        if self.get_dhatu_info(dhatu_info["dhatu"]):
            raise ValueError(f"Dhatu '{dhatu_info['dhatu']}' already exists.")
        self.data.setdefault("Dhatus", []).append(dhatu_info)
        self.save_data()

    def update_dhatu(self, dhatu, new_dhatu_info):
        self.validate_dhatu_info(new_dhatu_info)
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

    def search_dhatus(self, **criteria):
        results = self.data.get("Dhatus", [])
        for key, value in criteria.items():
            results = [dhatu_info for dhatu_info in results if dhatu_info.get(key) == value]
        return results

    def count_dhatus(self):
        return len(self.data.get("Dhatus", []))

    def list_unique_ganas(self):
        return list(set(dhatu_info.get("gana") for dhatu_info in self.data.get("Dhatus", [])))

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
        print("Meaning:", dhatu_info.get("meaning"))
        print("Tense Usage:", dhatu_info.get("tense_usage"))

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
        "example_usage": "धातवः",
        "meaning": "to hold, to support",
        "tense_usage": {
            "present": "धारयति",
            "past": "अधारयत्",
            "future": "धारयिष्यति"
        }
    }
    dhatu_kosha.add_dhatu(new_dhatu_info)

    # Update an existing dhatu
    updated_dhatu_info = {
        "dhatu": "कृ",
        "gana": "तिङ्",
        "lakshana": "कार्य",
        "example_usage": "कर्तुं कारणे, कर्मणि विधिः. Updated example usage.",
        "meaning": "to do, to make",
        "tense_usage": {
            "present": "करोति",
            "past": "चकार",
            "future": "करिष्यति"
        }
    }
    dhatu_kosha.update_dhatu("कृ", updated_dhatu_info)

    # Delete a dhatu
    dhatu_kosha.delete_dhatu("धा")

    # Search dhatus by multiple criteria
    search_results = dhatu_kosha.search_dhatus(gana="तिङ्", lakshana="कार्य")
    print("Search Results:", search_results)

    # Count the number of dhatus
    print("Total Dhatus:", dhatu_kosha.count_dhatus())

    # List all unique ganas
    print("Unique Ganas:", dhatu_kosha.list_unique_ganas())
