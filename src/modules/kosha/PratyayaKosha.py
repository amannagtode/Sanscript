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
            return {"metadata": {}, "Pratyayas": []}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.filepath}")
            return {"metadata": {}, "Pratyayas": []}

    def save_data(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def validate_pratyaya_info(self, pratyaya_info):
        required_keys = ["pratyaya", "gana", "vibhakti", "meaning", "example_usage"]
        for key in required_keys:
            if key not in pratyaya_info:
                raise ValueError(f"Missing required key: {key}")
        return True

    def get_pratyaya_info(self, pratyaya):
        for pratyaya_info in self.data.get("Pratyayas", []):
            if pratyaya_info.get("pratyaya") == pratyaya:
                return pratyaya_info
        return None

    def get_all_pratyayas(self):
        return [pratyaya_info.get("pratyaya") for pratyaya_info in self.data.get("Pratyayas", [])]

    def get_pratyayas_by_vibhakti(self, vibhakti):
        return [pratyaya_info for pratyaya_info in self.data.get("Pratyayas", []) if pratyaya_info.get("vibhakti") == vibhakti]

    def get_pratyayas_by_gana(self, gana):
        return [pratyaya_info for pratyaya_info in self.data.get("Pratyayas", []) if pratyaya_info.get("gana") == gana]

    def add_pratyaya(self, pratyaya_info):
        self.validate_pratyaya_info(pratyaya_info)
        if self.get_pratyaya_info(pratyaya_info["pratyaya"]):
            raise ValueError(f"Pratyaya '{pratyaya_info['pratyaya']}' already exists.")
        self.data.setdefault("Pratyayas", []).append(pratyaya_info)
        self.save_data()

    def update_pratyaya(self, pratyaya, new_pratyaya_info):
        self.validate_pratyaya_info(new_pratyaya_info)
        pratyayas = self.data.get("Pratyayas", [])
        for idx, pratyaya_info in enumerate(pratyayas):
            if pratyaya_info.get("pratyaya") == pratyaya:
                pratyayas[idx] = new_pratyaya_info
                self.data["Pratyayas"] = pratyayas
                self.save_data()
                return True
        raise ValueError(f"Pratyaya '{pratyaya}' not found.")

    def delete_pratyaya(self, pratyaya):
        pratyayas = self.data.get("Pratyayas", [])
        for idx, pratyaya_info in enumerate(pratyayas):
            if pratyaya_info.get("pratyaya") == pratyaya:
                del pratyayas[idx]
                self.data["Pratyayas"] = pratyayas
                self.save_data()
                return True
        raise ValueError(f"Pratyaya '{pratyaya}' not found.")

    def search_pratyayas(self, **criteria):
        results = self.data.get("Pratyayas", [])
        for key, value in criteria.items():
            results = [pratyaya_info for pratyaya_info in results if pratyaya_info.get(key) == value]
        return results

    def count_pratyayas(self):
        return len(self.data.get("Pratyayas", []))

    def list_unique_vibhaktis(self):
        return list(set(pratyaya_info.get("vibhakti") for pratyaya_info in self.data.get("Pratyayas", [])))

    def check_for_duplicates(self):
        pratyayas = self.data.get("Pratyayas", [])
        seen = set()
        duplicates = []
        for pratyaya_info in pratyayas:
            pratyaya = pratyaya_info.get("pratyaya")
            if pratyaya in seen:
                duplicates.append(pratyaya)
            else:
                seen.add(pratyaya)
        return duplicates

    def export_to_csv(self, filepath):
        try:
            import csv
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["pratyaya", "gana", "vibhakti", "meaning", "example_usage"])
                for pratyaya_info in self.data.get("Pratyayas", []):
                    writer.writerow([pratyaya_info.get("pratyaya"), pratyaya_info.get("gana"), pratyaya_info.get("vibhakti"), pratyaya_info.get("meaning"), pratyaya_info.get("example_usage")])
        except Exception as e:
            print(f"Error exporting to CSV: {e}")

    def import_from_csv(self, filepath):
        try:
            import csv
            with open(filepath, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.add_pratyaya(row)
        except Exception as e:
            print(f"Error importing from CSV: {e}")

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
        print("-", pratyaya)

    # Search pratyayas by vibhakti
    vibhakti_pratyayas = pratyaya_kosha.get_pratyayas_by_vibhakti("तृतीया")
    print("Pratyayas in Tṛtīyā Vibhakti:")
    for pratyaya in vibhakti_pratyayas:
        print("-", pratyaya.get("pratyaya"))

    # Add a new pratyaya
    new_pratyaya_info = {
        "pratyaya": "ण्",
        "gana": "तिङ्",
        "vibhakti": "तृतीया",
        "meaning": "denotes the third case (dative)",
        "example_usage": "लिखणं"
    }
    pratyaya_kosha.add_pratyaya(new_pratyaya_info)

    # Update an existing pratyaya
    updated_pratyaya_info = {
        "pratyaya": "ण्",
        "gana": "तिङ्",
        "vibhakti": "तृतीया",
        "meaning": "denotes the third case (dative). Updated meaning.",
        "example_usage": "लिखणं"
    }
    pratyaya_kosha.update_pratyaya("ण्", updated_pratyaya_info)

    # Delete a pratyaya
    pratyaya_kosha.delete_pratyaya("ण्")

    # Search pratyayas by multiple criteria
    search_results = pratyaya_kosha.search_pratyayas(gana="तिङ्", vibhakti="तृतीया")
    print("Search Results:", search_results)

    # Count the number of pratyayas
    print("Total Pratyayas:", pratyaya_kosha.count_pratyayas())

    # List all unique vibhaktis
    print("Unique Vibhaktis:", pratyaya_kosha.list_unique_vibhaktis())

    # Check for duplicate pratyayas
    duplicates = pratyaya_kosha.check_for_duplicates()
    print("Duplicate Pratyayas:", duplicates)

    # Export pratyayas to CSV
    pratyaya_kosha.export_to_csv("pratyayas.csv")

    # Import pratyayas from CSV
    pratyaya_kosha.import_from_csv("pratyayas.csv")
