class SamvadaVyavastha:
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
