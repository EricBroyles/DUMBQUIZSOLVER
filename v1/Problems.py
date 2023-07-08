import re
import os
import datetime
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
from helpers import clean_text

from FormatText import FormatText


class Problems:

    """
    Assumes:
    * all probelem data is in image format
    * prob_text is NOT already cleaned -> still has newlines, punctuation, stop words
    * No Header or Footer: ALL TEXT IS A Question OR AN Answer
    * All questions must end with punctuation [. , ! ? : ]
    * Questions and Answers may have punctutation throughout text
    * Answers must not end with punctuation 
    * Bullets will be interpret as some non [a-zA-Z0-9] character ie () or @, etc
    * Once Question and Answers are found they are cleaned -> remove newlines, punctuation, stop words

    """

    def __init__(self, problems_path):

        self.prob_text = self.getImgText(problems_path)
        unclean_questions, unclean_answers = self.getQA()
        self.format_text = FormatText(problems_path)
        self.format_text.setQA(unclean_questions, unclean_answers)

        self.questions, self.answers = self.format_text.getQA()

    def getImgText(self, path):
        img = cv2.imread(path)
        text = pytesseract.image_to_string(img)
        return text

    def getQA(self):
        """
        algorithm for getting the unclean questions and answers from the image
        """

        text = self.prob_text

        ques = []
        answ = []

        


        return ques, answ

    

#V1
# class Problems:
#     questions = []  # List of text
#     answers = []  # List of arrays

#     def __init__(self, prob_text):
#         self.getQA(prob_text)

#     def __str__(self):
#         result = "Problems: \n"
    
#         for i,q in enumerate(self.questions):
#             result += str(i+1) + ") " + q + "\n"
#             for k, a in enumerate(self.answers[i]):
#                 letter = chr(k + ord('a'))
#                 result += "\t" + letter + ") " + a + "\n"

#             result += "\n"

#         return result

#     def getQA(self, prob_text):
#         # Preprocess the problem text
#         pre_lines = prob_text.split("\n")
#         lines = pre_lines.copy()

#         for line in pre_lines:
#             if line == "":
#                 lines.pop(0)
#             else:
#                 break

#         index_of_first_line_end = 0
#         index_of_first_empty_line = lines.index("")
#         for i, line in enumerate(lines):

#             if line.strip()[-1] in ['.', '!', '?', ':']:
#                 index_of_first_line_end = i
#                 break
        

#         # Remove header if it exists
#         if index_of_first_line_end > index_of_first_empty_line:
#             print("Removed Header: ", lines[0:index_of_first_empty_line+1])
#             lines[0:index_of_first_empty_line+1] = []

#         lines = [line for line in lines if line]  # Remove all empty lines

#         is_question = False
#         current_question = ""
#         current_answers = []

#         for line in lines:
#             if is_question and line[0].isalpha():
#                 current_question += line + " "
#             elif line[0].isalpha():
#                 is_question = True
#                 current_question += line + " "
#                 if current_answers:
#                     self.answers.append(current_answers)
#                     current_answers = []
#             else:
#                 current_answers.append(clean_text(line))

#             if not line[-1].isalpha():
#                 if current_question:
#                     self.questions.append(clean_text(current_question))
#                 current_question = ""
#                 is_question = False

#         if current_answers:
#             self.answers.append(current_answers)
        

    
    



