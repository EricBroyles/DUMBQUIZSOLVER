import re
import os
import datetime
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from helpers import clean_text

class FormatText:

    """
    Format_text -> stored under folder problems with the same name as the passed image

    *********************************************************************************

    Created: (datetime of created, updated when overwritten)
    Edited: (y/n) as in edited by the user, if not flipped to y notifie user if change detect and then overrides

    *********************************************************************************

    +++++ UNCLEAN +++++

    {_Q_} the question text goes here uncleaned to be used as input for clean
    {__A} any answers go here
    {__A} etc...
    {__A} 
    {__A}

    {_Q_}
    {__A}
    {__A}
    

    !!!!! REFERENCE ONLY (edits to "clean" will be ignored) !!!!!
    ----- CLEAN -----

    {_Q_} the question text goes here cleaned to be used by algo
    {__A} any answers go here
    {__A} etc...
    {__A} 
    {__A}

    {_Q_}
    {__A}
    {__A}
    
    """

    def __init__(self, path):
        self.format_text_path = self.convertPath(path)
        self.unclean_ques = []
        self.unclean_answ = []
        self.clean_ques = []
        self.clean_answ = []

        self.format_text = self.getFormatText()


    def setQA(self, ques, answ):
        self.clean_answ = []
        self.clean_ques = []
        self.unclean_ques = ques
        self.unclean_answ = answ

        for item in ques:
            self.clean_ques.append(clean_text(item))

        for item in answ:
            temp = []
            for a in item:
                temp.append(clean_text(a))

            self.clean_answ.append(temp)

    def getFormatText(self):
        file_text = ""

        if self.doesExist():
            with open(self.format_text_path, "r") as file:
                file_text = file.read()

        return file_text

    def convertPath(self, path):
        """
        converts any path into what it should be for the Format_text, ie makes extension .txt
        """
        return re.sub(r'\.\w+$', '', path) + ".txt"

    def doesExist(self):
        """
        path can be any path with any extension that matches the location of the file
        all Format_Texts will end with .txt
        """
        return os.path.exists(self.format_text_path )
    
    def getEditStatus(self):
        """
        0: false it has not been edited or created
        1: it has been edited and flagged properly by user, do not override
        2: it has been edited but not flagged by user -> prompt user to confirm
        returns 0, 1, 2
        """
        if self.doesExist():

            #extract the edit status
            datetime_created, edited_flag = self.getHeaderInfo()

            if edited_flag == "y":
                return 1
            
            last_edit_timestamp = os.path.getmtime(self.format_text_path )
            last_modified = datetime.datetime.fromtimestamp(last_edit_timestamp)

            #to ignore the difference that occurs when writing to the file on creation
            if (last_modified - datetime_created).total_seconds() >= 5:
                return 2
        else:
            return 0
    

    ##WHY U NO WORK?????
    
    def setEditFlag(self, input_text):
        """
        Sets the "edited" flag to the provided input_text.
        """
        print("editing flag")
        # Read the file contents
        with open(self.format_text_path, "r") as file:
            lines = file.readlines()

        print(lines)
        # Update the "edited" flag
        for i, line in enumerate(lines):
            if line.strip().startswith("Edited:"):
                print("edit found")
                lines[i] = f"Edited: {input_text}\n"
                print(lines[i])
                break

        # Write the updated contents back to the file
        with open(self.format_text_path, "w") as file:
            file.writelines(lines)

    def getHeaderInfo(self):
        text = self.format_text
       
        # Extract created datetime
        created_match = re.search(r"Created: (.+)", text)
        created_datetime = None

        if created_match:
            created_str = created_match.group(1)
            created_datetime = datetime.datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")

        # Extract edited flag
        edited_match = re.search(r"Edited: (\w)", text)
        edited_flag = None

        if edited_match:
            edited_flag = edited_match.group(1).lower()

        return created_datetime, edited_flag
    
    def getQA(self, type):
        """
        type: "CLEAN" or "UNCLEAN"
        gets for just the clean text
        """
        unclean = r"\+\+\+\+\+ UNCLEAN \+\+\+\+\+\n(.+?)(?=\n-+ CLEAN -+)"
        clean = r"(?:\n-+ CLEAN -+\n)\s*(.*)"
        pattern = clean if type == "CLEAN" else unclean
        text = re.search(pattern, self.format_text, re.DOTALL).group(1)

        print(text)

        questions = []
        answers = []

        curr_ques = None
        curr_answs = []

        lines = text.split('\n')

        for line in lines:
            #found a question
            if line.startswith('{_Q_}'):
                # New question found
                if curr_ques:
                    # Save the previous question and its answers
                    questions.append(curr_ques)
                    answers.append(curr_answs)
                # Reset variables for the new question
                curr_ques = line.replace('{_Q_}', '').strip()
                curr_answs = []

            #found a answer
            elif line.startswith('{__A}'):
                # New answer found
                answer = line.replace('{__A}', '').strip()
                curr_answs.append(answer)

            #found an extension, for an answer or question, or nothing
            else:
                ext = line.strip()
                if ext:
                    if not curr_answs:
                        #keep adding this text to the question
                        curr_ques += " " + ext
                    else:
                        #keep adding this text to the last answer
                        curr_answs[-1] += " " + ext
        if curr_ques:
            questions.append(curr_ques)
            answers.append(curr_answs)

        return questions, answers
    
    def createFormatText(self, edit_flag):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        unclean_text = f"\n+++++ UNCLEAN +++++\n"
        for i,q in enumerate(self.unclean_ques):
            unclean_text += '\n{_Q_} ' + q

            for a in self.unclean_answ[i]:
                unclean_text += "\n"
                unclean_text += '{__A} ' + a
            unclean_text += "\n"
            
        clean_text = f"\n\n!!!!! REFERENCE ONLY (edits to CLEAN will be ignored) !!!!!\n----- CLEAN -----\n"
        for i,q in enumerate(self.clean_ques):
            clean_text += '\n{_Q_} ' + q

            for a in self.clean_answ[i]:
                clean_text += "\n"
                clean_text += '{__A} ' + a
            clean_text += "\n"

        header = f"""
*********************************************************************************

Created: {timestamp}
Edited: {edit_flag}

*********************************************************************************
        """

        self.format_text = header + unclean_text + clean_text

    def writeToPath(self):
        text = self.format_text
        with open(self.format_text_path, "w") as file:
            file.write(text)
    
    def createFormatTextFile(self):
        """
        perform the following checks with getEditStatus
        """
        edit_flag = "n"

        #checks
        status = self.getEditStatus()

        if status == 2:
            print("ACTION REQUIRED")
            print("The file ", self.format_text_path, " appear to have been edited and not flagged")
            ans = input("Would you like to override this file (y/n): ")
            if ans == "n":
                print("Keeping changes and updating clean. Flagging Document as Edited.")
                q, a = self.getQA("UNCLEAN")
                edit_flag ="y"
                self.setQA(q, a)
            else:
                print('Override.')
        if status == 1:
            return 0
    
        #create the text
        self.createFormatText(edit_flag)

        #write to the file path
        self.writeToPath()
        return 1

        
        




