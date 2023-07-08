
import re
import math
from helpers import remove_punc, isTFAnswer, find_closest_number





class Solutions:
    problems = None
    source = None
    solutions = []
    reasons = []

    def __init__(self, problems, source):
        self.problems = problems
        self.source = source
        self.solve()


    def __str__(self):
        result = "SOLVING \n"
        
        for i, q in enumerate(self.problems.questions):
            result += str(i+1) + ") " + q + "\n"
            result += "\t=================================================\n"
            for k, a in enumerate(self.problems.answers[i]):
                letter = chr(k + ord('a'))
                result += "\t" + letter + ") " + a + "\n"
                result += "\t\tMatches: " + str(self.solutions[i][k]) + "\n"
            result += "\t-------------------------------------------------\n"
            result += "\tRational: " + "\n"
            result += "\t\t" + self.reasons[i] + "\n"
            result += "\t=================================================\n"

            result += "\n"

        return result
    
    def solve(self):
        ques = self.problems.questions
        anws = self.problems.answers
        
        for i,q in enumerate(ques):
            q_sols = []
            center_context = None

            for k,a in enumerate(anws[i]):
                a_sol = None
                a_type = isTFAnswer(a) #strings "True", "False", or None if not a true or false answer

                if a_type is None:
                    a_sol, center_context = self.find(a, q)
                else:
                    a_sol, center_context = self.find(q, q)
                    if a_type == "False": a_sol = 1 - a_sol

                q_sols.append(a_sol)

            self.solutions.append(q_sols)
            self.reasons.append(self.findReasons(center_context))

    def find(self, search, context):
        #DO NOT MAKE THE SOURCE A SET, IT NEEDS TO RETAIN THE LOCATION AND NUMBER OF WORDS OF ANY TYPE
        #can make the ques and answs set, may not want to tho

        source = self.source.text

        #define the context location as an index
        context_center = self.findContextCenter(context)

        #search through the source to find all indexes of each seach word
        match_indexes = self.search(search, context_center, source)

        #find the score by making indexes close to the context_center worth more
        scr = self.score(match_indexes, context_center)
        # print("FIND")
        # print(search)
        # print(context_center)
        # print(match_indexes)
        # print(scr)
        # print()
        return scr, context_center
    
    def findReasons(self, center):
        reason = ""

        source = self.source.text
        source_words = source.split()

        for i in range(round(center) - 10, round(center) + 10):
            reason += source_words[i] + " "

        return reason

    def score(self, indexes, center):
        sigma = 200
        val = 0

        for i in indexes:
            val += math.exp(-((i - center) ** 2) / (2 * sigma ** 2))

        return val


    def search(self, search, center, findin):
        match_indexes = [] #indexes for each word that match
        #only wants to retunr the match_index closest to the center

        search_words = search.split()
        findin_words = findin.split()

        for word in search_words:
            matches = [index for index, value in enumerate(findin_words) if value == word]
            if len(matches):
                match_indexes += [find_closest_number(matches, center)]
            
        return match_indexes

    def findContextCenter(self, context):

        #DO NOT MAKE THE SOURCE A SET, IT NEEDS TO RETAIN THE LOCATION AND NUMBER OF WORDS OF ANY TYPE
        #can make the ques and answs set, may not want to tho

        #context weighting: if the word is unique (has fewer ocurrences) it should have a greater influence on the average index

        source = self.source.text
        context_indexes = [] #index average of where the context items were located
        context_counts = []
        total_count = 0

        source_words = source.split()
        context_words = context.split()

        for word in context_words:
            
            new_context_indexes = [index for index, value in enumerate(source_words) if value == word]
            context_count = source_words.count(word)
            total_count += context_count
            new_context_counts = [context_count] * len(new_context_indexes)

            context_indexes += new_context_indexes
            context_counts += new_context_counts

        weight_indexes = []
        for i, index in enumerate(context_indexes):
            weight = (context_counts[i] / total_count)
            if weight > 0:
                weight_indexes += [index] * round(1 / weight)

        context_indexes += weight_indexes

        context_center = sum(context_indexes) / len(context_indexes)

        return context_center

