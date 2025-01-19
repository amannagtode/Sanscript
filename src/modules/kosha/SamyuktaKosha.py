import os
import logging
import json
from jsonschema import validate, ValidationError
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SamyuktaKosha:
    def __init__(self, filepath):
        self.filepath = filepath
        self.schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "SamyuktaKosha",
            "type": "object",
            "properties": {
                "entries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "word": { "type": "string" },
                            "meaning": { "type": "string" },
                            "examples": {
                                "type": "array",
                                "items": { "type": "string" }
                            },
                            "synonyms": {
                                "type": "array",
                                "items": { "type": "string" }
                            },
                            "metadata": {
                                "type": "object",
                                "properties": {
                                    "created_at": { "type": "string", "format": "date-time" },
                                    "updated_at": { "type": "string", "format": "date-time" }
                                }
                            }
                        },
                        "required": ["word", "meaning"]
                    }
                }
            },
            "required": ["entries"]
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
            return {"entries": []}
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {self.filepath}")
            return {"entries": []}
        except ValidationError as e:
            logger.error(f"JSON validation error: {e.message}")
            return {"entries": []}
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return {"entries": []}

    def save_data(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving data: {e}")

    def validate_entry(self, entry):
        required_keys = ["word", "meaning"]
        for key in required_keys:
            if key not in entry:
                raise ValueError(f"Missing required key: {key}")
        return True

    def add_entry(self, entry):
        self.validate_entry(entry)
        if self.get_entry(entry["word"]):
            raise ValueError(f"Entry for word '{entry['word']}' already exists.")
        entry["metadata"] = {
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        self.data["entries"].append(entry)
        self.save_data()

    def get_entry(self, word):
        for entry in self.data["entries"]:
            if entry["word"] == word:
                return entry
        return None

    def update_entry(self, word, new_entry):
        self.validate_entry(new_entry)
        for idx, entry in enumerate(self.data["entries"]):
            if entry["word"] == word:
                new_entry["metadata"] = entry.get("metadata", {})
                new_entry["metadata"]["updated_at"] = datetime.utcnow().isoformat()
                self.data["entries"][idx] = new_entry
                self.save_data()
                return True
        return False

    def delete_entry(self, word):
        for idx, entry in enumerate(self.data["entries"]):
            if entry["word"] == word:
                del self.data["entries"][idx]
                self.save_data()
                return True
        return False

    def search_entries(self, **criteria):
        results = self.data["entries"]
        for key, value in criteria.items():
            results = [entry for entry in results if entry.get(key) == value]
        return results

    def list_all_words(self):
        return [entry["word"] for entry in self.data["entries"]]

    def backup_data(self, backup_filepath):
        try:
            with open(backup_filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            logger.info(f"Backup created at {backup_filepath}")
        except Exception as e:
            logger.error(f"Error creating backup: {e}")

    def restore_data(self, backup_filepath):
        try:
            with open(backup_filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                validate(instance=data, schema=self.schema)
                self.data = data
                self.save_data()
            logger.info(f"Data restored from {backup_filepath}")
        except FileNotFoundError:
            logger.error(f"Error: Backup file not found at {backup_filepath}")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {backup_filepath}")
        except ValidationError as e:
            logger.error(f"JSON validation error: {e.message}")
        except Exception as e:
            logger.error(f"Error restoring data: {e}")

# Example usage
if __name__ == "__main__":
    kosha = SamyuktaKosha("SamyuktaKosha.json")

    # Add a new entry
    new_entry = {
        "word": "धर्म",
        "meaning": "Righteousness, duty",
        "examples": ["धर्मः एव हि एकः", "धर्मेणैव हि जीवनम्"],
        "synonyms": ["नीति", "सदाचार"]
    }
    kosha.add_entry(new_entry)

    # Get an entry
    entry = kosha.get_entry("धर्म")
    print("Entry for 'धर्म':", entry)

    # Update an entry
    updated_entry = {
        "word": "धर्म",
        "meaning": "Righteousness, duty, law",
        "examples": ["धर्मः एव हि एकः", "धर्मेणैव हि जीवनम्"],
        "synonyms": ["नीति", "सदाचार", "न्याय"]
    }
    kosha.update_entry("धर्म", updated_entry)

    # Delete an entry
    kosha.delete_entry("धर्म")

    # Search entries
    search_results = kosha.search_entries(meaning="Righteousness, duty, law")
    print("Search results:", search_results)

    # List all words
    all_words = kosha.list_all_words()
    print("All words:", all_words)

    # Backup data
    kosha.backup_data("SamyuktaKosha_backup.json")

    # Restore data
    kosha.restore_data("SamyuktaKosha_backup.json")
import os
import logging
import json
from jsonschema import validate, ValidationError
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SamyuktaKosha:
    def __init__(self, filepath):
        self.filepath = filepath
        self.schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "SamyuktaKosha",
            "type": "object",
            "properties": {
                "entries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "word": { "type": "string" },
                            "meaning": { "type": "string" },
                            "examples": {
                                "type": "array",
                                "items": { "type": "string" }
                            },
                            "synonyms": {
                                "type": "array",
                                "items": { "type": "string" }
                            },
                            "metadata": {
                                "type": "object",
                                "properties": {
                                    "created_at": { "type": "string", "format": "date-time" },
                                    "updated_at": { "type": "string", "format": "date-time" }
                                }
                            }
                        },
                        "required": ["word", "meaning"]
                    }
                }
            },
            "required": ["entries"]
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
            return {"entries": []}
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {self.filepath}")
            return {"entries": []}
        except ValidationError as e:
            logger.error(f"JSON validation error: {e.message}")
            return {"entries": []}
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return {"entries": []}

    def save_data(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error saving data: {e}")

    def validate_entry(self, entry):
        required_keys = ["word", "meaning"]
        for key in required_keys:
            if key not in entry:
                raise ValueError(f"Missing required key: {key}")
        return True

    def add_entry(self, entry):
        self.validate_entry(entry)
        if self.get_entry(entry["word"]):
            raise ValueError(f"Entry for word '{entry['word']}' already exists.")
        entry["metadata"] = {
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        self.data["entries"].append(entry)
        self.save_data()

    def get_entry(self, word):
        for entry in self.data["entries"]:
            if entry["word"] == word:
                return entry
        return None

    def update_entry(self, word, new_entry):
        self.validate_entry(new_entry)
        for idx, entry in enumerate(self.data["entries"]):
            if entry["word"] == word:
                new_entry["metadata"] = entry.get("metadata", {})
                new_entry["metadata"]["updated_at"] = datetime.utcnow().isoformat()
                self.data["entries"][idx] = new_entry
                self.save_data()
                return True
        return False

    def delete_entry(self, word):
        for idx, entry in enumerate(self.data["entries"]):
            if entry["word"] == word:
                del self.data["entries"][idx]
                self.save_data()
                return True
        return False

    def search_entries(self, **criteria):
        results = self.data["entries"]
        for key, value in criteria.items():
            results = [entry for entry in results if entry.get(key) == value]
        return results

    def list_all_words(self):
        return [entry["word"] for entry in self.data["entries"]]

    def backup_data(self, backup_filepath):
        try:
            with open(backup_filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            logger.info(f"Backup created at {backup_filepath}")
        except Exception as e:
            logger.error(f"Error creating backup: {e}")

    def restore_data(self, backup_filepath):
        try:
            with open(backup_filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                validate(instance=data, schema=self.schema)
                self.data = data
                self.save_data()
            logger.info(f"Data restored from {backup_filepath}")
        except FileNotFoundError:
            logger.error(f"Error: Backup file not found at {backup_filepath}")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from {backup_filepath}")
        except ValidationError as e:
            logger.error(f"JSON validation error: {e.message}")
        except Exception as e:
            logger.error(f"Error restoring data: {e}")

# Example usage
if __name__ == "__main__":
    kosha = SamyuktaKosha("SamyuktaKosha.json")

    # Add a new entry
    new_entry = {
        "word": "धर्म",
        "meaning": "Righteousness, duty",
        "examples": ["धर्मः एव हि एकः", "धर्मेणैव हि जीवनम्"],
        "synonyms": ["नीति", "सदाचार"]
    }
    kosha.add_entry(new_entry)

    # Get an entry
    entry = kosha.get_entry("धर्म")
    print("Entry for 'धर्म':", entry)

    # Update an entry
    updated_entry = {
        "word": "धर्म",
        "meaning": "Righteousness, duty, law",
        "examples": ["धर्मः एव हि एकः", "धर्मेणैव हि जीवनम्"],
        "synonyms": ["नीति", "सदाचार", "न्याय"]
    }
    kosha.update_entry("धर्म", updated_entry)

    # Delete an entry
    kosha.delete_entry("धर्म")

    # Search entries
    search_results = kosha.search_entries(meaning="Righteousness, duty, law")
    print("Search results:", search_results)

    # List all words
    all_words = kosha.list_all_words()
    print("All words:", all_words)

    # Backup data
    kosha.backup_data("SamyuktaKosha_backup.json")

    # Restore data
    kosha.restore_data("SamyuktaKosha_backup.json")
