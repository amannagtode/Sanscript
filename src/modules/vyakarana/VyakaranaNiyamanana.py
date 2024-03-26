class VyakaranaNiyama {
  static readonly VakyaRule = {
    type: "sequence",
    elements: [
      { type: "Naama" },
      { type: "Kriya" },
      // Allow optional elements like Upasarga and Vibhakti (indirect object) # type: ignore
      { type: "Upasarga", optional: true },
      { type: "Vibhakti", optional: true },
    ],
  };

  static readonly NaamaRule = {
    type: "choice",
    elements: [
      { type: "SamjñaNaama", properties: { gender: String, number: String, case: String } },
      { type: "SarvaNaama", properties: { person: String, number: String, case: String } },
      // Add rules for pronouns and adjectives
    ],
  };

  static readonly KriyaRule = {
    type: "sequence",
    elements: [
      // Consider optional prefixes and augmentations
      { type: "Pratyaya", optional: true }, // for pre-fixes
      { type: "Dhātu", properties: { root: String, tense: String, voice: String } },
      { type: "Pratyaya", required: true }, // for main suffix
    ],
  };

  static readonly VibhaktiRule = {
    type: "choice",
    elements: [
      { type: "KarakaVibhakti", properties: { karaka: String } },
      { type: "TatpurushaSamasa", properties: { components: Array<String> } },
      // Add rules for other compound types and adpositional phrases
    ],
  };

  // ... Define additional rules for various grammatical elements

  // Function to validate a sentence against grammar rules
  static isValidSentence(sentence: Array<Object>): boolean {
    const vakyaIsValid = this.VakyaRule.validate(sentence);
    if (!vakyaIsValid) {
      return false;
    }

    // Perform further validations on individual elements and their properties
    for (const element of sentence) {
      const elementTypeRule = this[element.type + "Rule"];
      if (!elementTypeRule.validate(element)) {
        return false;
      }
    }

    return true;
  }

  // ... Implement validation functions for individual element types

}

// Example usage

const validSentence = [
  { type: "SamjñaNaama", value: "रामः", properties: { gender: "masculine", number: "singular", case: "nominative" } },
  { type: "Kriya", value: "दर्शयति", properties: { root: "दर्श", tense: "present", voice: "active" } },
  { type: "KarakaVibhakti", value: "कर्मणि", properties: { karaka: "object" } },
];

const invalidSentence = [
  { type: "Kriya", value: "दर्शति", properties: { root: "दर्श", tense: "past", voice: "active" } },
  { type: "SamjñaNaama", value: "सीता", properties: { gender: "feminine", number: "singular", case: "accusative" } },
];

console.log(VyakaranaNiyama.isValidSentence(validSentence) ? "Valid sentence!" : "Invalid sentence.");
console.log(VyakaranaNiyama.isValidSentence(invalidSentence) ? "Valid sentence!" : "Invalid sentence.");