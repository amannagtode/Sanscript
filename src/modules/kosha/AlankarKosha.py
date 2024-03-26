import os
import json

class AlankaraKosha:
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(__file__), "alankara_kosha.json")
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

    def get_alankara(self, name):
        for alankara in self.data.get("Alankaras", []):
            if alankara.get("name") == name:
                return alankara
        return None

    def get_alankaras_by_category(self, category):
        return [alankara for alankara in self.data.get("Alankaras", []) if alankara.get("category") == category]

    def get_alankaras_by_subcategory(self, subcategory):
        return [alankara for alankara in self.data.get("Alankaras", []) if subcategory in alankara.get("subcategories", [])]

    def get_alankaras_by_reference(self, reference):
        return [alankara for alankara in self.data.get("Alankaras", []) if reference in alankara.get("references", [])]

    def add_alankara(self, alankara):
        alankaras = self.data.get("Alankaras", [])
        alankaras.append(alankara)
        self.data["Alankaras"] = alankaras
        self.save_data()

    def update_alankara(self, name, new_alankara):
        alankaras = self.data.get("Alankaras", [])
        for idx, alankara in enumerate(alankaras):
            if alankara.get("name") == name:
                alankaras[idx] = new_alankara
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

    def save_data(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

# Example usage:
if __name__ == "__main__":
    alankara_kosha = AlankaraKosha()

    # Get information for a specific alankara
    alankara_info = alankara_kosha.get_alankara("Upamalarankara")
    if alankara_info:
        print("Definition:", alankara_info.get("definition"))
        print("Examples:")
        for example in alankara_info.get("examples", []):
            print("-", example)

    # Get information for all alankaras
    all_alankaras = alankara_kosha.get_all_alankaras()
    print("All Alankaras:")
    for alankara in all_alankaras:
        print("-", alankara.get("name"))

    # Search alankaras by category
    sabdalankara_alankaras = alankara_kosha.get_alankaras_by_category("Sabdalankara")
    print("Sabdalankara Alankaras:")
    for alankara in sabdalankara_alankaras:
        print("-", alankara.get("name"))

    # Add a new alankara
    new_alankara = {
        "name": "NewAlankara",
        "definition": "A new alankara added to the kosha.",
        "examples": ["New example 1", "New example 2"],
        "category": "Arthalankara",
        "subcategories": ["NewSubcategory"],
        "references": ["NewReference"]
    }
    alankara_kosha.add_alankara(new_alankara)

    # Update an existing alankara
    updated_alankara = {
        "name": "Upamalarankara",
        "definition": "A figure of speech in which a comparison is made between two unlike objects using words like 'iva' (like, as). Updated definition.",
        "examples": ["Updated example 1", "Updated example 2"],
        "category": "Sabdalankara",
        "subcategories": ["UpdatedSubcategory"],
        "references": ["UpdatedReference"]
    }
    alankara_kosha.update_alankara("Upamalarankara", updated_alankara)

    # Delete an alankara
    alankara_kosha.delete_alankara("NewAlankara")
