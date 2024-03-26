from collections import namedtuple
import re

# Constants
DEVANAGARI_ENCODING = "utf-8"
SAMYUKTA_Vowels = ("अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ")
SAMYUKTA_Consonants = ("क", "ख", "ग", "घ", "ङ", "च", "छ", "ज", "झ", "ञ", "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न", "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व", "श", "ष", "स", "ह", "क्ष", "त्र", "ज्ञ")

# Sandhi rule functions
def is_nasal_assimilated(char1, char2):
    return char1 in ("न", "म") and char2 in ("ग", "घ", "ज", "झ", "ड", "ढ", "ब", "भ")

def is_sandhi_deleted(char1, char2):
    return char1 == "त्" and char2 in ("च", "छ", "ट", "ठ", "त", "थ")

def is_visarga_to_vowel(char1, char2):
    return char1 == "ः" and char2 in SAMYUKTA_Vowels

# Consonant cluster dictionary (expand further as needed)
YUKTAH_KSHARA_DICT = {"क् + व": "क्व", "त् + व": "त्व", "त् + र": "त्र", "ष् + ठ": "ष्ट"}

# Function to identify all consonant clusters (not just YUKTAH_KSHARA)
def is_consonant_cluster(char1, char2):
    return char1 in SAMYUKTA_Consonants and char2 in SAMYUKTA_Consonants and (char1 + char2 not in YUKTAH_KSHARA_DICT)

# Expanded function to handle different cluster formations and sandhi rules
def handle_consonant_cluster(char1, char2):
    """
    Checks for different consonant cluster formations, applies relevant sandhi rules, and handles YUKTAH_KSHARA.

    Args:
      char1: The first consonant character.
      char2: The second consonant character.

    Returns:
      (str, bool): A tuple containing:
        - Combined syllable string if cluster formation or YUKTAH_KSHARA occurs, otherwise empty string.
        - True if a valid cluster or YUKTAH_KSHARA is formed, False otherwise.
    """

    # Ensure that char1 and char2 are in Devanagari script
    if char1 in DEVANAGARI_ENCODING and char2 in DEVANAGARI_ENCODING:

        # Blending: Combine characters with special diacritic
        if char1 == "क" and char2 == "च":
            return char1 + "\u094D" + char2, True
        if char1 == "प" and char2 == "त":
            return char1 + "\u094D" + char2, True
        if char1 == "भ" and char2 == "व":
            return char1 + "\u094D" + char2, True

        # Reduction: Simplify consonant combinations
        if char1 == "त" and char2 == "त":
            return "ट", True

        # Nasal Assimilation: Modify consonant based on following sound
        if char1 in ("न", "म") and char2 in ("ग", "घ", "ज", "झ", "ड", "ढ", "ब", "भ"):
            if char1 == "न" and char2 in ("ज", "झ"):
                return chr(ord(char1) + 32), False
            if char1 == "म" and char2 in ("ड", "ढ"):
                return chr(ord(char1) + 32), False
            return chr(ord(char1) + 32), True

        # Gemination: Duplicate consonant in specific contexts
        if char1 in ("त्", "थ"):
            if char1 == "त्" and char2 == "त":
                return char1 + char1, True
            if char1 == "थ" and char2 in ("थ", "द", "ध"):
                return char1 + char1, True

        # Sandhi deletion: Remove vowel due to preceding consonant
        if char1 == "त्" and char2 in ("च", "छ", "ट", "ठ", "त", "थ"):
            if char2 == "य":
                return char1 + char2, True
            return None, False

        # Visarga + Consonant clusters
        if char1 == "ः" and char2 in ("ट", "न"):
            if char2 == "ट":
                return char1 + char2, True
            elif char2 == "न":
                return char1 + char2, True

        # Dynamic YUKTAH_KSHARA rule check (based on the next character)
        if char2 in SAMYUKTA_Vowels:
            # Visarga + consonant + vowel: ष् + ट + अ becomes ष्ट, ष् + न + इ becomes क्ष्ण
            if char1 == "ष्" and char2 in ("ट", "न"):
                if char2 == "ट":
                    return char1 + char2, True
                elif char2 == "न":
                    return char1 + char2 + "्", True
            # Specific consonant + vowel transitions: क् + व + अ becomes क्व, त् + र + आ becomes त्र
            if char1 == "क्" and char2 == "व":
                return char1 + "्व", True
            if char1 == "त्" and char2 == "र":
                return char1 + "्र", True

        # Static YUKTAH_KSHARA lookup
        if (char1, char2) in YUKTAH_KSHARA_DICT:
            return YUKTAH_KSHARA_DICT[(char1, char2)], True  # type: ignore

    # Unhandled cluster: Return an empty string and False
    return "", False

def parse_sanskrit_string(text):
    """
    Parses a Sanskrit string into individual characters and syllables with stress and diacritics (implement later).

    Args:
      text: A string containing Sanskrit text.

    Returns:
      A list of tuples, where each tuple represents a syllable:
        (character, is_vowel, is_stressed, has_diacritic)
    """

    syllables = []
    i = 0
    while i < len(text):
        char = text[i]
        if char in DEVANAGARI_ENCODING:
            decoded_char = char.encode(DEVANAGARI_ENCODING).decode()
            # Initialize stress and diacritic status as False
            syllables.append((decoded_char, decoded_char in SAMYUKTA_Vowels, False, False))

        # Apply sandhi rules and update syllable information
        if i < len(text) - 1:
            current_char, next_char = text[i], text[i + 1]

            # Vowel + Vowel: Generally not allowed, except for diphthongs.
            if syllables[-1][1] and next_char in SAMYUKTA_Vowels:
                if current_char + next_char in ("एओ", "औ"):
                    syllables[-1] = (current_char + next_char, True, syllables[-1][2], syllables[-1][3])
                    i += 2  # Skip the next character as it has been merged into a single syllable
                    continue
                else:
                    # Invalid: Handle exception (e.g., sandhi errors)
                    # You may add your logic here for handling this case
                    i += 1

            # Consonant + Vowel: Most common case, check for nasal assimilation.
            elif not syllables[-1][1] and next_char in SAMYUKTA_Vowels:
                if is_nasal_assimilated(current_char, next_char):
                    syllables[-1] = (chr(ord(current_char) + 32), False, syllables[-1][2], syllables[-1][3])  # Modify consonant for assimilation
                # ... add other relevant sandhi rules for consonant + vowel interactions ...

            # Vowel + Consonant: Requires checking for consonant clusters, halant, and sandhi deletion.
            elif syllables[-1][1] and not next_char in SAMYUKTA_Vowels:
                if is_consonant_cluster(current_char, next_char):
                    # Handle different consonant cluster formation and sandhi rules using 'handle_consonant_cluster'
                    cluster_string, is_valid = handle_consonant_cluster(current_char, next_char)
                    if is_valid:
                        syllables[-1] = (cluster_string, True, syllables[-1][2], syllables[-1][3])  # Combine a valid cluster
                        i += 1  # Skip the next character as it has been merged into a single syllable
                        continue
                elif current_char == "अ" and next_char == "ः":
                    syllables[-1] = (current_char + next_char, True, syllables[-1][2], syllables[-1][3])  # Visarga following vowel
                elif is_sandhi_deleted(current_char, next_char):
                    syllables.pop()  # Delete vowel due to sandhi rule
                    i -= 1  # Reevaluate the current character as it has been popped
                else:
                    # Handle other vowel + consonant interactions and potential sandhi exceptions
                    # For example, you may add specific rules for combinations like ए + च, ओ + ण, etc.
                    # You can customize this section based on your specific requirements
                    i += 1

            # Consonant + Consonant: Less common, requires further sandhi rule implementation.
            elif not syllables[-1][1] and not next_char in SAMYUKTA_Vowels:
                # ... expand this section with additional rules and exceptions for various consonant cluster interactions ...
                # You may add your logic here for handling other cases
                i += 1

        i += 1

    # ... add code for optional stress and diacritic marking in the future

    return syllables

# Example usage
sanskrit_text = "नमस्ते"
parsed_syllables = parse_sanskrit_string(sanskrit_text)

# Further processing and analysis of parsed syllables
for syllable in parsed_syllables:
    print("Syllable:", syllable[0])
    print("Is Vowel:", syllable[1])
    print("Is Stressed:", syllable[2])
    print("Has Diacritic:", syllable[3])
    print()  # Add a newline for better readability

