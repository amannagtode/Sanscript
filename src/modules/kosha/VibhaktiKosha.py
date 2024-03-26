import os
import json

class VibhaktiKosha:
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(__file__), "vibhakti_kosha.json")
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

    def inflect_case(self, noun, case, number='singular'):
        for entry in self.data.get("Nouns", []):
            if entry["noun"] == noun:
                return entry[number].get(case, "Not found")
        return "Noun not found"

    def add_noun(self, noun, gender, singular_forms, plural_forms=None):
        existing_nouns = [entry["noun"] for entry in self.data.get("Nouns", [])]
        if noun in existing_nouns:
            print(f"Noun '{noun}' already exists.")
            return False
        new_noun = {"noun": noun, "gender": gender, "singular": singular_forms}
        if plural_forms:
            new_noun["plural"] = plural_forms
        self.data["Nouns"].append(new_noun)
        self.save_data()
        return True

    def save_data(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            print("Data saved successfully.")
        except Exception as e:
            print(f"Error saving data: {e}")

# Example usage:
if __name__ == "__main__":
    vibhakti_kosha = VibhaktiKosha()

    # Example of inflecting a noun for a specific case
    noun = "राम"
    case = "षष्ठी"
    inflected_noun = vibhakti_kosha.inflect_case(noun, case)
    print(f"Noun '{noun}' in '{case}' case:", inflected_noun)

    # Example of adding a new noun
    new_noun = "गोपाल"
    new_gender = "masculine"
    new_singular_forms = {
        "प्रथमा": "गोपालः",
        "द्वितीया": "गोपालम्",
        "तृतीया": "गोपालेन",
        "चतुर्थी": "गोपालस्य",
        "पञ्चमी": "गोपाले",
        "षष्ठी": "गोपालाय",
        "सप्तमी": "गोपाल"
    }
    if vibhakti_kosha.add_noun(new_noun, new_gender, new_singular_forms):
        print(f"Noun '{new_noun}' added successfully.")
    else:
        print(f"Failed to add noun '{new_noun}'.")
