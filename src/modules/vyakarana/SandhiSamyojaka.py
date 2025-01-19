import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SandhiSamyojaka:
    @staticmethod
    def apply_sandhi(word1: str, word2: str) -> str:
        """
        Apply sandhi rules between two Sanskrit words.

        Args:
            word1: The first Sanskrit word.
            word2: The second Sanskrit word.

        Returns:
            The combined word after applying sandhi rules.
        """
        if not word1 or not word2:
            logger.error("Both words must be provided")
            raise ValueError("Both words must be provided")

        if SandhiSamyojaka.is_vowel(word1[-1]) and SandhiSamyojaka.is_consonant(word2[0]):
            return SandhiSamyojaka.apply_vowel_consonant_sandhi(word1, word2)
        elif SandhiSamyojaka.is_consonant(word1[-1]) and SandhiSamyojaka.is_consonant(word2[0]):
            return SandhiSamyojaka.apply_consonant_consonant_sandhi(word1, word2)
        elif SandhiSamyojaka.is_vowel(word1[-1]) and SandhiSamyojaka.is_vowel(word2[0]):
            return SandhiSamyojaka.apply_vowel_vowel_sandhi(word1, word2)
        return word1 + " " + word2

    @staticmethod
    def is_vowel(char: str) -> bool:
        """
        Check if the given character is a vowel.

        Args:
            char: The character to check.

        Returns:
            True if the character is a vowel, False otherwise.
        """
        vowels = set(["अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ॠ", "ऌ", "ॡ", "ए", "ऐ", "ओ", "औ"])
        return char in vowels

    @staticmethod
    def is_consonant(char: str) -> bool:
        """
        Check if the given character is a consonant.

        Args:
            char: The character to check.

        Returns:
            True if the character is a consonant, False otherwise.
        """
        consonants = set(["क", "ख", "ग", "घ", "ङ", "च", "छ", "ज", "झ", "ञ", "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न", "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व", "श", "ष", "स", "ह"])
        return char in consonants

    @staticmethod
    def apply_vowel_consonant_sandhi(word1: str, word2: str) -> str:
        """
        Apply sandhi rules between a vowel and a consonant.

        Args:
            word1: The first word ending with a vowel.
            word2: The second word starting with a consonant.

        Returns:
            The combined word after applying sandhi rules.
        """
        vowel = word1[-1]
        consonant = word2[0]
        sandhi_map = {
            "अ": {"क": "अच्", "ख": "अग्", "ग": "अज्", "घ": "अज्", "ङ": "अञ्", "च": "च्", "छ": "च्", "ज": "ज्", "झ": "ज्", "ञ": "ञ्", "ट": "ट्", "ठ": "ट्", "ड": "ट्", "ढ": "ट्", "ण": "ण्", "त": "त्", "थ": "त्", "द": "त्", "ध": "त्", "न": "न्", "प": "प्", "फ": "प्", "ब": "प्", "भ": "प्", "म": "म्", "य": "य्", "र": "र्", "ल": "ल्", "व": "व्", "श": "श्", "ष": "ष्", "स": "स्", "ह": "ह्"}
        }
        combined = sandhi_map.get(vowel, {}).get(consonant, vowel + consonant)
        return word1[:-1] + combined + word2[1:]

    @staticmethod
    def apply_consonant_consonant_sandhi(word1: str, word2: str) -> str:
        """
        Apply sandhi rules between two consonants.

        Args:
            word1: The first word ending with a consonant.
            word2: The second word starting with a consonant.

        Returns:
            The combined word after applying sandhi rules.
        """
        consonant1 = word1[-1]
        consonant2 = word2[0]
        sandhi_map = {
            "क": {"त": "च्", "त्": "च्", "प": "प्"},
            "ख": {"त": "च्", "त्": "च्", "प": "प्"},
            "ग": {"त": "ज्", "त्": "ज्", "प": "ङ्"},
            "घ": {"त": "ज्", "त्": "ज्", "प": "ङ्"},
            "ङ": {"त": "ञ्", "त्": "ञ्", "प": "ञ्"},
            "च": {"त": "च्", "त्": "च्", "प": "प्"},
            "छ": {"त": "च्", "त्": "च्", "प": "प्"},
            "ज": {"त": "ज्", "त्": "ज्", "प": "ञ्"},
            "झ": {"त": "ज्", "त्": "ज्", "प": "ञ्"},
            "ट": {"त": "ट्", "त्": "ट्", "प": "प्"},
            "ठ": {"त": "ट्", "त्": "ट्", "प": "प्"},
            "ड": {"त": "ट्", "त्": "ट्", "प": "प्"},
            "ढ": {"त": "ट्", "त्": "ट्", "प": "प्"},
            "ण": {"त": "ण्", "त्": "ण्", "प": "न्"},
            "त": {"त": "त्", "त्": "त्", "प": "त्"},
            "थ": {"त": "त्", "त्": "त्", "प": "त्"},
            "द": {"त": "त्", "त्": "त्", "प": "त्"},
            "ध": {"त": "त्", "त्": "त्", "प": "त्"},
            "न": {"त": "न्", "त्": "न्", "प": "न्"},
            "प": {"त": "प्", "त्": "प्", "प": "प्"},
            "फ": {"त": "प्", "त्": "प्", "प": "प्"},
            "ब": {"त": "प्", "त्": "प्", "प": "प्"},
            "भ": {"त": "प्", "त्": "प्", "प": "प्"},
            "म": {"त": "म्", "त्": "म्", "प": "म्"},
            "य": {"त": "य्", "त्": "य्", "प": "य्"},
            "र": {"त": "र्", "त्": "र्", "प": "र्"},
            "ल": {"त": "ल्", "त्": "ल्", "प": "ल्"},
            "व": {"त": "व्", "त्": "व्", "प": "व्"},
            "श": {"त": "श्", "त्": "श्", "प": "श्"},
            "ष": {"त": "श्", "त्": "श्", "प": "ष्"},
            "स": {"त": "स्", "त्": "स्", "प": "स्"},
            "ह": {"त": "ह्", "त्": "ह्", "प": "ह्"}
        }
        combined = sandhi_map.get(consonant1, {}).get(consonant2, consonant1 + consonant2)
        return word1[:-1] + combined + word2[1:]

    @staticmethod
    def apply_vowel_vowel_sandhi(word1: str, word2: str) -> str:
        """
        Apply sandhi rules between two vowels.

        Args:
            word1: The first word ending with a vowel.
            word2: The second word starting with a vowel.

        Returns:
            The combined word after applying sandhi rules.
        """
        vowel1 = word1[-1]
        vowel2 = word2[0]
        sandhi_map = {
            "अ": {"अ": "आ", "इ": "ए", "उ": "ओ", "ऋ": "अर्", "ॠ": "अर्", "ऌ": "अल्", "ॡ": "अल्", "ए": "ऐ", "ऐ": "आ", "ओ": "औ", "औ": "आ"},
            "आ": {"अ": "आ", "इ": "ए", "उ": "ओ", "ऋ": "आर्", "ॠ": "आर्", "ऌ": "आल्", "ॡ": "आल्", "ए": "ऐ", "ऐ": "आ", "ओ": "औ", "औ": "आ"}
        }
        combined = sandhi_map.get(vowel1, {}).get(vowel2, vowel1 + vowel2)
        return word1[:-1] + combined + word2[1:]

# Example usage
if __name__ == "__main__":
    sandhi = SandhiSamyojaka()
    combined_word = sandhi.apply_sandhi("राम", "अर्जुनः")
    print("Combined Word:", combined_word)

    combined_word = sandhi.apply_sandhi("गङ्गा", "उदकः")
    print("Combined Word:", combined_word)

    combined_word = sandhi.apply_sandhi("देव", "इन्द्रः")
    print("Combined Word:", combined_word)

    combined_word = sandhi.apply_sandhi("कृष्ण", "बलरामः")
    print("Combined Word:", combined_word)
