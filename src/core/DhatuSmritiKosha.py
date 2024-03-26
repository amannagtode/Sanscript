import os
import json
import re
from collections import namedtuple
from dependency.SanskritLibrary import SanskritLibrary
from modules.kosha.VibhaktiKosha import VibhaktiKosha
from ShabdaSamyojaka import ShabdaSamyojaka

# Define Data Structures
DhātuInfo = namedtuple('DhātuInfo', ['root', 'gana', 'shai', 'lachhana', 'dhatupatha', 'pada', 'padapada'])
TaddhitaOptions = {}
LakaraOptions = {}

# Define Functions

def load_dhatu_data(filepath, validation_schema):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Validate and create DhātuInfo objects
            dhātu_info_objects = [DhātuInfo(**{key: validation_schema[key](verb.get(key, '')) for key in validation_schema}) for verb in data.get('verbs', [])]
            
            # Populate TaddhitaOptions and LakaraOptions based on your data structure
            
            return dhātu_info_objects
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filepath}")
    except Exception as e:
        print(f"Error loading data from {filepath}: {e}")
    return None

def get_verb_info(root, verb_info_list):
    return next((verb_info for verb_info in verb_info_list if verb_info.root == root), None)

def get_all_verbs(verb_info_list):
    return iter(verb_info_list)

def get_lakaras(verb_info, tense, mood, grammar_library):
    key = (verb_info, tense, mood)
    if key not in LakaraOptions:
        # Example logic to get valid lakaras using the SanskritLibrary
        valid_lakaras = grammar_library.get_valid_lakaras(verb_info, tense, mood)
        LakaraOptions[key] = valid_lakaras
    return LakaraOptions.get(key, set())

def get_taddhita_options(stem):
    return TaddhitaOptions.get(stem, set())

def conjugate_verb(verb_info, tense, mood, person, number, grammar_library):
    # Use grammar library to conjugate the verb
    conjugated_verb = grammar_library.conjugate_verb(verb_info.root, tense, mood, person, number)
    return conjugated_verb

def analyze_conjugated_verb(conjugated_verb, grammar_library):
    # Use grammar library to analyze the conjugated verb
    analysis = grammar_library.analyze_conjugated_verb(conjugated_verb)
    return analysis

def search_verbs(pattern, search_fields, verb_info_list):
    pattern = re.compile(pattern, re.IGNORECASE)  # Case insensitive search
    return [verb_info for verb_info in verb_info_list if any(pattern.search(getattr(verb_info, field)) for field in search_fields)]

def inflect_verb_case(conjugated_verb, case, grammar_library):
    # Use VibhaktiKosha for case inflection
    inflected_verb = grammar_library.inflect_verb_case(conjugated_verb, case)
    return inflected_verb

def apply_sandhi(conjugated_verb, grammar_library):
    # Use ShabdaSamyojaka for sandhi processing
    final_verb = grammar_library.apply_sandhi(conjugated_verb)
    return final_verb

# Example Usage (continued)
if __name__ == "__main__":
    # Load data from DhātuSmriti file
    validation_schema = {"root": str, "gana": str, "shai": str, "lachhana": str, "dhatupatha": str, "pada": str, "padapada": str}
    dhātu_smriti_data = load_dhatu_data("path/to/data.json", validation_schema)

    if dhātu_smriti_data:
        verb_info_list = dhātu_smriti_data

        # Get information for verb "gam"
        verb_info = get_verb_info("gam", verb_info_list)

        if verb_info:
            # Check valid lakaras for present tense, indicative mood
            valid_lakaras = get_lakaras(verb_info, "present", "indicative", SanskritLibrary())

            # Conjugate verb in present tense, indicative mood, 3rd person singular
            conjugated_verb = conjugate_verb(verb_info, "present", "indicative", 3, "singular", SanskritLibrary())

            # Analyze conjugated verb for details
            analysis = analyze_conjugated_verb(conjugated_verb, SanskritLibrary())

            # Search verbs containing "pat" in their root or dhatupatha
            verbs_with_pat = search_verbs("pat", ["root", "dhatupatha"], verb_info_list)

            # Inflect the conjugated verb in accusative case
            inflected_verb = inflect_verb_case(conjugated_verb, "accusative", SanskritLibrary())

            # Apply sandhi to the inflected verb
            final_verb = apply_sandhi(inflected_verb, SanskritLibrary())

            # Print the results
            print("Valid Lakaras:", valid_lakaras)
            print("Conjugated Verb:", conjugated_verb)
            print("Analysis:", analysis)
            print("Verbs containing 'pat':", verbs_with_pat)
            print("Inflected Verb (Accusative Case):", inflected_verb)
            print("Final Verb (After Sandhi):", final_verb)
