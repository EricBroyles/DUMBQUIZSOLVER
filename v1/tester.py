# import re

# # def clean_string(input_string):
# #     # Replace special non-alphabetical characters with a space
# #     cleaned_string = re.sub(r'[^a-zA-Z]', ' ', input_string)
    
# #     # Remove leading and trailing spaces
# #     cleaned_string = cleaned_string.strip()
    
# #     # Convert the string to lowercase
# #     cleaned_string = cleaned_string.lower()
    
# #     return cleaned_string

# # # Test the function
# # input_str = "Hello, World! 123"
# # cleaned_str = clean_string(input_str)
# # print(cleaned_str)  # Output: hello world

# pattern = r'^(?:Tue|True|Tu)$'

# # Example usage
# string1 = "Tue"    # Matches
# string2 = "True"   # Matches
# string3 = "Tu"     # Matches
# string4 = "T"      # Does not match
# string5 = "Txxe"   # Does not match
# string6 = "Tr"     # Does not match

# match1 = re.match(r'^(?:Tue|True|Tu)$', string1) is not None
# match2 = re.match(pattern, string2) is not None
# match3 = re.match(pattern, string3) is not None
# match4 = re.match(pattern, string4) is not None
# match5 = re.match(pattern, string5) is not None
# match6 = re.match(pattern, string6) is not None

# print(match1)  # True
# print(match2)  # True
# print(match3)  # True
# print(match4)  # False
# print(match5)  # False
# print(match6)  # False

# import re

# text = "This is a sample text! It contains some punctuation marks, and special characters @#$%^&*()."

# # Remove all punctuation and special characters
# cleaned_text = re.sub(r'[^\w\s]', '', text)

# print(cleaned_text)


import re
import datetime

input_text = """
    *********************************************************************************
    Created: 2022-01-01 10:30:00
    Edited: Yes
    *********************************************************************************
"""

# Extract created datetime
created_match = re.search(r"Created: (.+)", input_text)
created_datetime = None

if created_match:
    created_str = created_match.group(1)
    created_datetime = datetime.datetime.strptime(created_str, "%Y-%m-%d %H:%M:%S")

# Extract edited flag
edited_match = re.search(r"Edited: (\w)", input_text)
edited_flag = None

if edited_match:
    edited_flag = edited_match.group(1)

print("Created:", created_datetime)
print("Edited:", edited_flag)

text = """
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

{_Q_} the question text goes here cleaned to be used by algoghgh
jhsdhjgdkfds
{__A} any answers go here
hhgj
{__A} etc...
{__A} some
{__A} other

{_Q_} another q
{__A} pain
here I am
{__A} ghhg
"""

def getQA(text):
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








    # current_question = None
    # current_answers = []

    # lines = text.split('\n')
    # for line in lines:
    #     if line.startswith('{_Q_}'):
    #         # New question found
    #         if current_question:
    #             # Save the previous question and its answers
    #             questions.append(current_question)
    #             answers.append(current_answers)
    #         # Reset variables for the new question
    #         current_question = line.replace('{_Q_}', '').strip()
    #         current_answers = []
    #     elif line.startswith('{__A}'):
    #         # New answer found
    #         answer = line.replace('{__A}', '').strip()
    #         current_answers.append(answer)
    #     else:
    #         #text has overflowed the line
    #         if not current_answers and questions:
    #             #keep adding this text to the question
    #             print("questions", questions)
    #             curr = questions[-1] + " " + line.strip()
    #             questions[-1] = curr
    #         elif current_answers and current_answers[-1]:
    #             #keep adding this text to the last answer
    #             curr = answers[-1][-1] + " " + line.strip()
    #             answers[-1][-1] = curr

    # # Add the last question and its answers
    # if current_question:
    #     questions.append(current_question)
    #     answers.append(current_answers)

    # return questions, answers
clean_section = re.search(r"----- CLEAN -----\n(.+)", text, re.DOTALL)
q, a = getQA(clean_section.group(1))
print(q)
print(a)

# answers = []

# clean_section = re.search(r"----- CLEAN -----\n(.+)", text, re.DOTALL)

# print(clean_section.group(1))

# lines = clean_section.group(1)

# for line in lines:







# if clean_section:
#     clean_text = clean_section.group(1)
#     question_matches = re.findall(r"\{\_Q\_\}(.+?)(?=\{\_Q\_\}|\{__A\}|\Z)", clean_text, re.DOTALL)
#     questions = [question.strip() for question in question_matches]

# answers = []

# clean_section = re.search(r"----- CLEAN -----\n(.+)", text, re.DOTALL)
# if clean_section:
#     clean_text = clean_section.group(1)
#     ans = re.findall(r"(?<=\{__A\})(.*?)(?=\{__A\}|\{_Q_\})", clean_text, re.DOTALL)
#     answers = [answer.strip() for answer in ans]


# print(questions)
# print(answers)

