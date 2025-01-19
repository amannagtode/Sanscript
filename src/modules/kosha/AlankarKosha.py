import os
    import os
    import json
    import logging
    from jsonschema import validate, ValidationError

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    class AlankaraKosha:
        def __init__(self):
            self.filepath = os.path.join(os.path.dirname(__file__), "AlankaraKosha.json")
            self.schema = {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": "AlankaraKosha",
                "type": "object",
                "properties": {
                    "Alankaras": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": { "type": "string" },
                                "definition": { "type": "string" },
                                "examples": {
                                    "type": "array",
                                    "items": { "type": "string" }
                                },
                                "category": { "type": "string" },
                                "subcategories": {
                                    "type": "array",
                                    "items": { "type": "string" }
                                },
                                "references": {
                                    "type": "array",
                                    "items": { "type": "string" }
                                }
                            },
                            "required": ["name", "definition", "examples", "category"]
                        }
                    }
                },
                "required": ["Alankaras"]
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

        def validate_alankara_info(self, alankara_info):
            required_keys = ["name", "definition", "examples", "category"]
            for key in required_keys:
                if key not in alankara_info:
                    raise ValueError(f"Missing required key: {key}")
            return True

        def get_alankara(self, name):
            for alankara in self.data.get("Alankaras", []):
                if alankara.get("name") == name:
                    return alankara
            return None

        def get_all_alankaras(self):
            return [alankara.get("name") for alankara in self.data.get("Alankaras", [])]

        def get_alankaras_by_category(self, category):
            return [alankara for alankara in self.data.get("Alankaras", []) if alankara.get("category") == category]

        def get_alankaras_by_subcategory(self, subcategory):
            return [alankara for alankara in self.data.get("Alankaras", []) if subcategory in alankara.get("subcategories", [])]

        def get_alankaras_by_reference(self, reference):
            return [alankara for alankara in self.data.get("Alankaras", []) if reference in alankara.get("references", [])]

        def add_alankara(self, alankara_info):
            self.validate_alankara_info(alankara_info)
            if self.get_alankara(alankara_info["name"]):
                raise ValueError(f"Alankara '{alankara_info['name']}' already exists.")
            self.data.setdefault("Alankaras", []).append(alankara_info)
            self.save_data()

        def update_alankara(self, name, new_alankara_info):
            self.validate_alankara_info(new_alankara_info)
            alankaras = self.data.get("Alankaras", [])
            for idx, alankara in enumerate(alankaras):
                if alankara.get("name") == name:
                    alankaras[idx] = new_alankara_info
                    self.data["Alankaras"] = alankaras
                    self.save_data()
                    return True
            return False

        def delete_alankara(self, name):
            alankaras = self.data.get("Alankaras", [])
            for idx, alankara in enumerate(alankaras):
                if alankara.get("name") == name:
                    del alankaras[idx]
                    self.data["Alankaras"] = alankaras
                    self.save_data()
                    return True
            return False

        def search_alankaras(self, **criteria):
            results = self.data.get("Alankaras", [])
            for key, value in criteria.items():
                results = [alankara for alankara in results if alankara.get(key) == value]
            return results

        def count_alankaras(self):
            return len(self.data.get("Alankaras", []))

        def list_unique_categories(self):
            return list(set(alankara.get("category") for alankara in self.data.get("Alankaras", [])))

        def list_unique_subcategories(self):
            subcategories = set()
            for alankara in self.data.get("Alankaras", []):
                subcategories.update(alankara.get("subcategories", []))
            return list(subcategories)

    # Example usage:
    if __name__ == "__main__":
        alankara_kosha = AlankaraKosha()

        # Get information for a specific alankara
        alankara_info = alankara_kosha.get_alankara("Upamalarankara")
        if alankara_info:
            print("Name:", alankara_info.get("name"))
            print("Definition:", alankara_info.get("definition"))
            print("Examples:", alankara_info.get("examples"))
            print("Category:", alankara_info.get("category"))
            print("Subcategories:", alankara_info.get("subcategories"))
            print("References:", alankara_info.get("references"))

        # Get information for all alankaras
        all_alankaras = alankara_kosha.get_all_alankaras()
        print("All Alankaras:")
        for alankara in all_alankaras:
            print("-", alankara)

        # Search alankaras by category
        category_alankaras = alankara_kosha.get_alankaras_by_category("Sabdalankara")
        print("Alankaras in 'Sabdalankara' category:")
        for alankara in category_alankaras:
            print("-", alankara.get("name"))

        # Add a new alankara
        new_alankara_info = {
            "name": "NewAlankara",
            "definition": "A new alankara added to the kosha.",
            "examples": ["New example 1", "New example 2"],
            "category": "Arthalankara",
            "subcategories": ["NewSubcategory"],
            "references": ["NewReference"]
        }
        alankara_kosha.add_alankara(new_alankara_info)

        # Update an existing alankara
        updated_alankara_info = {
            "name": "Upamalarankara",
            "definition": "A figure of speech in which a comparison is made between two unlike objects using words like 'iva' (like, as). Updated definition.",
            "examples": ["Updated example 1", "Updated example 2"],
            "category": "Sabdalankara",
            "subcategories": ["UpdatedSubcategory"],
            "references": ["UpdatedReference"]
        }
        alankara_kosha.update_alankara("Upamalarankara", updated_alankara_info)

        # Delete an alankara
        alankara_kosha.delete_alankara("NewAlankara")

        # Search alankaras by multiple criteria
        search_results = alankara_kosha.search_alankaras(category="Sabdalankara", subcategories="Uttarakalama")
        print("Search Results:", search_results)

        # Count the number of alankaras
        print("Total Alankaras:", alankara_kosha.count_alankaras())

        # List all unique categories
        print("Unique Categories:", alankara_kosha.list_unique_categories())

        # List all unique subcategories
        print("Unique Subcategories:", alankara_kosha.list_unique_subcategories())
import json

class AlankaraKosha:
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(__file__), "AlankaraKosha.json")
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

    def validate_alankara_info(self, alankara_info):
        required_keys = ["name", "definition", "examples", "category"]
        for key in required_keys:
            if key not in alankara_info:
                raise ValueError(f"Missing required key: {key}")
        return True

    def get_alankara(self, name):
        for alankara in self.data.get("Alankaras", []):
            if alankara.get("name") == name:
                return alankara
        return None

    def get_all_alankaras(self):
        return [alankara.get("name") for alankara in self.data.get("Alankaras", [])]

    def get_alankaras_by_category(self, category):
        return [alankara for alankara in self.data.get("Alankaras", []) if alankara.get("category") == category]

    def get_alankaras_by_subcategory(self, subcategory):
        return [alankara for alankara in self.data.get("Alankaras", []) if subcategory in alankara.get("subcategories", [])]

    def get_alankaras_by_reference(self, reference):
        return [alankara for alankara in self.data.get("Alankaras", []) if reference in alankara.get("references", [])]

    def add_alankara(self, alankara_info):
        self.validate_alankara_info(alankara_info)
        if self.get_alankara(alankara_info["name"]):
            raise ValueError(f"Alankara '{alankara_info['name']}' already exists.")
        self.data.setdefault("Alankaras", []).append(alankara_info)
        self.save_data()

    def update_alankara(self, name, new_alankara_info):
        self.validate_alankara_info(new_alankara_info)
        alankaras = self.data.get("Alankaras", [])
        for idx, alankara in enumerate(alankaras):
            if alankara.get("name") == name:
                alankaras[idx] = new_alankara_info
                self.data["Alankaras"] = alankaras
                self.save_data()
                return True
        return False

    def delete_alankara(self, name):
        alankaras = self.data.get("Alankaras", [])
        for idx, alankara in enumerate(alankaras):
            if alankara.get("name") == name:
                del alankaras[idx]
                self.data["Alankaras"] = alankaras
                self.save_data()
                return True
        return False

    def search_alankaras(self, **criteria):
        results = self.data.get("Alankaras", [])
        for key, value in criteria.items():
            results = [alankara for alankara in results if alankara.get(key) == value]
        return results

    def count_alankaras(self):
        return len(self.data.get("Alankaras", []))

    def list_unique_categories(self):
        return list(set(alankara.get("category") for alankara in self.data.get("Alankaras", [])))

    def list_unique_subcategories(self):
        subcategories = set()
        for alankara in self.data.get("Alankaras", []):
            subcategories.update(alankara.get("subcategories", []))
        return list(subcategories)

# Example usage:
if __name__ == "__main__":
    alankara_kosha = AlankaraKosha()

    # Get information for a specific alankara
    alankara_info = alankara_kosha.get_alankara("Upamalarankara")
    if alankara_info:
        print("Name:", alankara_info.get("name"))
        print("Definition:", alankara_info.get("definition"))
        print("Examples:", alankara_info.get("examples"))
        print("Category:", alankara_info.get("category"))
        print("Subcategories:", alankara_info.get("subcategories"))
        print("References:", alankara_info.get("references"))

    # Get information for all alankaras
    all_alankaras = alankara_kosha.get_all_alankaras()
    print("All Alankaras:")
    for alankara in all_alankaras:
        print("-", alankara)

    # Search alankaras by category
    category_alankaras = alankara_kosha.get_alankaras_by_category("Sabdalankara")
    print("Alankaras in 'Sabdalankara' category:")
    for alankara in category_alankaras:
        print("-", alankara.get("name"))

    # Add a new alankara
    new_alankara_info = {
        "name": "NewAlankara",
        "definition": "A new alankara added to the kosha.",
        "examples": ["New example 1", "New example 2"],
        "category": "Arthalankara",
        "subcategories": ["NewSubcategory"],
        "references": ["NewReference"]
    }
    alankara_kosha.add_alankara(new_alankara_info)

    # Update an existing alankara
    updated_alankara_info = {
        "name": "Upamalarankara",
        "definition": "A figure of speech in which a comparison is made between two unlike objects using words like 'iva' (like, as). Updated definition.",
        "examples": ["Updated example 1", "Updated example 2"],
        "category": "Sabdalankara",
        "subcategories": ["UpdatedSubcategory"],
        "references": ["UpdatedReference"]
    }
    alankara_kosha.update_alankara("Upamalarankara", updated_alankara_info)

    # Delete an alankara
    alankara_kosha.delete_alankara("NewAlankara")

    # Search alankaras by multiple criteria
    search_results = alankara_kosha.search_alankaras(category="Sabdalankara", subcategories="Uttarakalama")
    print("Search Results:", search_results)

    # Count the number of alankaras
    print("Total Alankaras:", alankara_kosha.count_alankaras())

    # List all unique categories
    print("Unique Categories:", alankara_kosha.list_unique_categories())

    # List all unique subcategories
    print("Unique Subcategories:", alankara_kosha.list_unique_subcategories())
