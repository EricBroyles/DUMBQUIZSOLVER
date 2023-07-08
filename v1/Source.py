from helpers import clean_text

class Source:
    lines = []
    text = "" #all the clean text, is an string of words sep by " " 
    def __init__(self, file_path):
        self.lines = self.extractLines(file_path)
        text = ""
        for line in self.lines:
            text += (clean_text(line)) + " "
        self.text = text

    def __str__(self):
        return self.text

    def extractLines(self, file_path):
        lines = []
        with open(file_path, 'r') as file:
            for line in file:
                lines.append(line.strip().lower())
        return lines