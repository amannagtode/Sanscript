class SamvadaVyavastha:
    import logging
    import json
    from datetime import datetime

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    class SamvadaVyavastha:
        def __init__(self):
            self.dialogue = {}
            self.history = []

        def create_dialogue(self, speakers):
            """
            Creates a dialogue structure with specified speakers.
            
            Args:
                speakers (list): List of speakers in the dialogue.
            """
            for speaker in speakers:
                self.dialogue[speaker] = []
            logger.info(f"Created dialogue with speakers: {speakers}")

        def add_speaker(self, speaker_name):
            """
            Adds a new speaker to the dialogue.
            
            Args:
                speaker_name (str): Name of the new speaker.
            """
            if speaker_name not in self.dialogue:
                self.dialogue[speaker_name] = []
                logger.info(f"Added speaker: {speaker_name}")
            else:
                logger.warning(f"Speaker '{speaker_name}' already exists.")

        def remove_speaker(self, speaker_name):
            """
            Removes a speaker from the dialogue.
            
            Args:
                speaker_name (str): Name of the speaker to be removed.
            """
            if speaker_name in self.dialogue:
                del self.dialogue[speaker_name]
                logger.info(f"Removed speaker: {speaker_name}")
            else:
                logger.warning(f"Speaker '{speaker_name}' does not exist.")

        def modify_dialogue(self, speaker_name, new_dialogue):
            """
            Modifies the dialogue of a specific speaker.
            
            Args:
                speaker_name (str): Name of the speaker whose dialogue is to be modified.
                new_dialogue (list): New dialogue lines for the specified speaker.
            """
            if speaker_name in self.dialogue:
                self.dialogue[speaker_name] = new_dialogue
                logger.info(f"Modified dialogue for speaker: {speaker_name}")
            else:
                logger.warning(f"Speaker '{speaker_name}' does not exist.")

        def display_dialogue(self):
            """
            Displays the entire dialogue.
            """
            for speaker, lines in self.dialogue.items():
                print(f"{speaker}:")
                for line in lines:
                    print(f"\t{line}")

        def add_dialogue_line(self, speaker_name, new_line):
            """
            Adds a new line to the dialogue of the specified speaker.
            
            Args:
                speaker_name (str): Name of the speaker.
                new_line (str): New line to be added to the dialogue.
            """
            if speaker_name in self.dialogue:
                self.dialogue[speaker_name].append(new_line)
                self.history.append((datetime.utcnow(), speaker_name, new_line))
                logger.info(f"Added dialogue line for speaker: {speaker_name}")
            else:
                logger.warning(f"Speaker '{speaker_name}' does not exist.")

        def remove_dialogue_line(self, speaker_name, line_index):
            """
            Removes a line from the dialogue of the specified speaker.
            
            Args:
                speaker_name (str): Name of the speaker.
                line_index (int): Index of the line to be removed.
            """
            if speaker_name in self.dialogue:
                if 0 <= line_index < len(self.dialogue[speaker_name]):
                    del self.dialogue[speaker_name][line_index]
                    logger.info(f"Removed dialogue line {line_index} for speaker: {speaker_name}")
                else:
                    logger.warning(f"Invalid line index for speaker '{speaker_name}'.")
            else:
                logger.warning(f"Speaker '{speaker_name}' does not exist.")

        def export_dialogue(self, filepath):
            """
            Exports the dialogue to a JSON file.
            
            Args:
                filepath (str): Path to the file where the dialogue will be saved.
            """
            try:
                with open(filepath, 'w', encoding='utf-8') as file:
                    json.dump(self.dialogue, file, ensure_ascii=False, indent=4)
                logger.info(f"Dialogue exported to {filepath}")
            except Exception as e:
                logger.error(f"Error exporting dialogue: {e}")

        def import_dialogue(self, filepath):
            """
            Imports the dialogue from a JSON file.
            
            Args:
                filepath (str): Path to the file from which the dialogue will be loaded.
            """
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    self.dialogue = json.load(file)
                logger.info(f"Dialogue imported from {filepath}")
            except FileNotFoundError:
                logger.error(f"Error: File not found at {filepath}")
            except json.JSONDecodeError:
                logger.error(f"Error decoding JSON from {filepath}")
            except Exception as e:
                logger.error(f"Error importing dialogue: {e}")

        def search_dialogue(self, keyword):
            """
            Searches for a keyword in the dialogue.
            
            Args:
                keyword (str): The keyword to search for.
            
            Returns:
                list: A list of tuples containing the speaker and the line where the keyword was found.
            """
            results = []
            for speaker, lines in self.dialogue.items():
                for line in lines:
                    if keyword in line:
                        results.append((speaker, line))
            logger.info(f"Found {len(results)} occurrences of keyword '{keyword}'")
            return results

        def get_dialogue_history(self):
            """
            Returns the history of added dialogue lines.
            
            Returns:
                list: A list of tuples containing the timestamp, speaker, and dialogue line.
            """
            return self.history

    # Example usage:
    if __name__ == "__main__":
        samvada_vyavastha = SamvadaVyavastha()

        # Create a dialogue with two speakers
        samvada_vyavastha.create_dialogue(["रामः", "कृष्णः"])

        # Add a new speaker
        samvada_vyavastha.add_speaker("अर्जुनः")

        # Remove a speaker
        samvada_vyavastha.remove_speaker("रामः")

        # Modify the dialogue of a speaker
        samvada_vyavastha.modify_dialogue("कृष्णः", ["भगवानुवाच:", "सुखदुःखे समे कृत्वा...", "तत्विप्रवृत्तिम् न कर्माणि..."])

        # Add a new line to the dialogue
        samvada_vyavastha.add_dialogue_line("कृष्णः", "सम्प्राप्तयोधः शुकं पश्यति।")

        # Remove a line from the dialogue
        samvada_vyavastha.remove_dialogue_line("कृष्णः", 1)

        # Display the dialogue
        samvada_vyavastha.display_dialogue()

        # Export the dialogue to a JSON file
        samvada_vyavastha.export_dialogue("dialogue.json")

        # Import the dialogue from a JSON file
        samvada_vyavastha.import_dialogue("dialogue.json")

        # Search for a keyword in the dialogue
        search_results = samvada_vyavastha.search_dialogue("भगवानुवाच")
        print("Search results:", search_results)

        # Get the dialogue history
        history = samvada_vyavastha.get_dialogue_history()
        print("Dialogue history:", history)
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    class DialogueManager:
        def __init__(self):
            self.dialogues = []

        def add_dialogue(self, speaker, text):
            """
            Add a dialogue to the dialogue manager.

            Args:
                speaker (str): The name of the speaker.
                text (str): The text of the dialogue.

            Returns:
                None
            """
            if not speaker or not text:
                logger.error("Speaker and text must be provided")
                raise ValueError("Speaker and text must be provided")
            
            dialogue = {"speaker": speaker, "text": text}
            self.dialogues.append(dialogue)
            logger.info(f"Added dialogue: {dialogue}")

        def get_all_dialogues(self):
            """
            Get all dialogues.

            Returns:
                list: A list of all dialogues.
            """
            return self.dialogues

        def search_dialogues_by_speaker(self, speaker):
            """
            Search dialogues by speaker.

            Args:
                speaker (str): The name of the speaker to search for.

            Returns:
                list: A list of dialogues by the specified speaker.
            """
            if not speaker:
                logger.error("Speaker must be provided")
                raise ValueError("Speaker must be provided")
            
            result = [dialogue for dialogue in self.dialogues if dialogue["speaker"] == speaker]
            logger.info(f"Found {len(result)} dialogues by speaker: {speaker}")
            return result

        def delete_dialogue(self, index):
            """
            Delete a dialogue by index.

            Args:
                index (int): The index of the dialogue to delete.

            Returns:
                None
            """
            try:
                deleted_dialogue = self.dialogues.pop(index)
                logger.info(f"Deleted dialogue: {deleted_dialogue}")
            except IndexError:
                logger.error(f"Index {index} out of range")
                raise IndexError(f"Index {index} out of range")

    # Example usage
    if __name__ == "__main__":
        manager = DialogueManager()
        
        # Add dialogues
        manager.add_dialogue("Alice", "Hello, how are you?")
        manager.add_dialogue("Bob", "I'm good, thank you!")
        
        # Get all dialogues
        all_dialogues = manager.get_all_dialogues()
        print("All Dialogues:", all_dialogues)
        
        # Search dialogues by speaker
        alice_dialogues = manager.search_dialogues_by_speaker("Alice")
        print("Dialogues by Alice:", alice_dialogues)
        
        # Delete a dialogue
        manager.delete_dialogue(0)
        print("All Dialogues after deletion:", manager.get_all_dialogues())
    def __init__(self):
        self.dialogue = {}

    def create_dialogue(self, speakers):
        """
        Creates a dialogue structure with specified speakers.
        
        Args:
            speakers (list): List of speakers in the dialogue.
        """
        for speaker in speakers:
            self.dialogue[speaker] = []

    def add_speaker(self, speaker_name):
        """
        Adds a new speaker to the dialogue.
        
        Args:
            speaker_name (str): Name of the new speaker.
        """
        if speaker_name not in self.dialogue:
            self.dialogue[speaker_name] = []
        else:
            print(f"Speaker '{speaker_name}' already exists.")

    def remove_speaker(self, speaker_name):
        """
        Removes a speaker from the dialogue.
        
        Args:
            speaker_name (str): Name of the speaker to be removed.
        """
        if speaker_name in self.dialogue:
            del self.dialogue[speaker_name]
        else:
            print(f"Speaker '{speaker_name}' does not exist.")

    def modify_dialogue(self, speaker_name, new_dialogue):
        """
        Modifies the dialogue of a specific speaker.
        
        Args:
            speaker_name (str): Name of the speaker whose dialogue is to be modified.
            new_dialogue (list): New dialogue lines for the specified speaker.
        """
        if speaker_name in self.dialogue:
            self.dialogue[speaker_name] = new_dialogue
        else:
            print(f"Speaker '{speaker_name}' does not exist.")

    def display_dialogue(self):
        """
        Displays the entire dialogue.
        """
        for speaker, lines in self.dialogue.items():
            print(f"{speaker}:")
            for line in lines:
                print(f"\t{line}")

    def add_dialogue_line(self, speaker_name, new_line):
        """
        Adds a new line to the dialogue of the specified speaker.
        
        Args:
            speaker_name (str): Name of the speaker.
            new_line (str): New line to be added to the dialogue.
        """
        if speaker_name in self.dialogue:
            self.dialogue[speaker_name].append(new_line)
        else:
            print(f"Speaker '{speaker_name}' does not exist.")

    def remove_dialogue_line(self, speaker_name, line_index):
        """
        Removes a line from the dialogue of the specified speaker.
        
        Args:
            speaker_name (str): Name of the speaker.
            line_index (int): Index of the line to be removed.
        """
        if speaker_name in self.dialogue:
            if 0 <= line_index < len(self.dialogue[speaker_name]):
                del self.dialogue[speaker_name][line_index]
            else:
                print(f"Invalid line index for speaker '{speaker_name}'.")
        else:
            print(f"Speaker '{speaker_name}' does not exist.")

# Example usage:
if __name__ == "__main__":
    samvada_vyavastha = SamvadaVyavastha()

    # Create a dialogue with two speakers
    samvada_vyavastha.create_dialogue(["रामः", "कृष्णः"])

    # Add a new speaker
    samvada_vyavastha.add_speaker("अर्जुनः")

    # Remove a speaker
    samvada_vyavastha.remove_speaker("रामः")

    # Modify the dialogue of a speaker
    samvada_vyavastha.modify_dialogue("कृष्णः", ["भगवानुवाच:", "सुखदुःखे समे कृत्वा...", "तत्विप्रवृत्तिम् न कर्माणि..."])

    # Add a new line to the dialogue
    samvada_vyavastha.add_dialogue_line("कृष्णः", "सम्प्राप्तयोधः शुकं पश्यति।")

    # Remove a line from the dialogue
    samvada_vyavastha.remove_dialogue_line("कृष्णः", 1)

    # Display the dialogue
    samvada_vyavastha.display_dialogue()
