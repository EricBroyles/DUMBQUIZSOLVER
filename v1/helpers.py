import re
import nltk

from nltk.corpus import stopwords

nltk.download("stopwords")

#Input: words -- a single string that may contain punctuation
#Output: a single string without any punctuation
def remove_punc(words):
    return re.sub(r'[^\w ]', '', words)

#remove all special chars and punctuation
#remove all stop words
def clean_text(text):
    all_rm_punc = re.sub(r'[^\w\s]', '', text)
    tok_low = all_rm_punc.split(" ")
    filt_tok = [tok for tok in tok_low if tok not in stopwords.words("english")]
    all_no_stop = " ".join(filt_tok)
    return all_no_stop.lower()

def find_closest_number(numbers, center):
    closest_number = None
    min_difference = float('inf')  # Initialize with a large value
    for num in numbers:
        difference = abs(num - center)

        if difference < min_difference:
            min_difference = difference
            closest_number = num

    return closest_number


def isTFAnswer(answer):

    answer = answer.strip()
    
    # Check if the answer is one word
    if len(answer.split()) != 1:
        return None
    
    if re.match(r'^(?:Tue|True|Tu)$', answer, re.IGNORECASE) is not None:
        return "True"
    
    if re.match(r'^(?:False|Fal|Fa)$', answer, re.IGNORECASE) is not None:
        return "False"
    else:
        return None
    

