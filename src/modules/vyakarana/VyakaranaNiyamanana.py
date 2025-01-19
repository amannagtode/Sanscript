import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VyakaranaNiyama:
    VakyaRule = {
        "type": "sequence",
        "elements": [
            {"type": "Naama"},
            {"type": "Kriya"},
            {"type": "Upasarga", "optional": True},
            {"type": "Vibhakti", "optional": True},
        ],
    }

    NaamaRule = {
        "type": "choice",
        "elements": [
            {"type": "SamjñaNaama", "properties": {"gender": str, "number": str, "case": str}},
            {"type": "SarvaNaama", "properties": {"person": str, "number": str, "case": str}},
        ],
    }

    KriyaRule = {
        "type": "sequence",
        "elements": [
            {"type": "Pratyaya", "optional": True},
            {"type": "Dhātu", "properties": {"root": str, "tense": str, "voice": str}},
            {"type": "Pratyaya", "required": True},
        ],
    }

    VibhaktiRule = {
        "type": "choice",
        "elements": [
            {"type": "KarakaVibhakti", "properties": {"karaka": str}},
            {"type": "TatpurushaSamasa", "properties": {"components": list}},
        ],
    }

    @staticmethod
    def isValidSentence(sentence):
        """
        Validate a sentence against the defined grammar rules.

        Args:
            sentence (list): A list of elements representing the sentence.

        Returns:
            bool: True if the sentence is valid, False otherwise.
        """
        try:
            vakyaIsValid = VyakaranaNiyama.validate_rule(sentence, VyakaranaNiyama.VakyaRule)
            if not vakyaIsValid:
                return False

            for element in sentence:
                elementTypeRule = getattr(VyakaranaNiyama, element["type"] + "Rule", None)
                if elementTypeRule and not VyakaranaNiyama.validate_rule(element, elementTypeRule):
                    return False

            return True
        except Exception as e:
            logger.error(f"Error validating sentence: {e}")
            return False

    @staticmethod
    def validate_rule(element, rule):
        """
        Validate an element against a specific rule.

        Args:
            element (dict): The element to validate.
            rule (dict): The rule to validate against.

        Returns:
            bool: True if the element is valid, False otherwise.
        """
        if rule["type"] == "sequence":
            for rule_elem in rule["elements"]:
                if rule_elem.get("optional") and not any(elem["type"] == rule_elem["type"] for elem in element):
                    continue
                if not any(elem["type"] == rule_elem["type"] for elem in element):
                    return False
        elif rule["type"] == "choice":
            if not any(element["type"] == choice["type"] for choice in rule["elements"]):
                return False
        return True

# Example usage
if __name__ == "__main__":
    validSentence = [
        {"type": "SamjñaNaama", "value": "रामः", "properties": {"gender": "masculine", "number": "singular", "case": "nominative"}},
        {"type": "Kriya", "value": "दर्शयति", "properties": {"root": "दर्श", "tense": "present", "voice": "active"}},
        {"type": "KarakaVibhakti", "value": "कर्मणि", "properties": {"karaka": "object"}},
    ]

    invalidSentence = [
        {"type": "Kriya", "value": "दर्शति", "properties": {"root": "दर्श", "tense": "past", "voice": "active"}},
        {"type": "SamjñaNaama", "value": "सीता", "properties": {"gender": "feminine", "number": "singular", "case": "accusative"}},
    ]

    print("Valid sentence:", VyakaranaNiyama.isValidSentence(validSentence))
    print("Invalid sentence:", VyakaranaNiyama.isValidSentence(invalidSentence))
