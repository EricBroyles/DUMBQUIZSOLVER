
import os
from Problems import Problems
from Source import Source
from Solutions import Solutions


#name coursemodule_Lesson_imagepartifneeded ie 1_1_1
print("Enter Number ie 1 to run through all 1_* items")
print("Or 1_1 to run all of 1_1 answers")
current_search_code = input("Enter Code: ")

if len(current_search_code) == 1:

    current_search_code += "_1"
    my_source = None
    my_problem = None

    while current_search_code:

        source_path = "source/" + current_search_code + ".txt"
        problems_path = "problems/" + current_search_code + ".png"

        #problem has occured if cant find the source of the form *_1
        if os.path.exists(source_path):
            my_source = Source(source_path)
        else:
            print()
            print("DONE or")
            print("Error: failed to find the source path ->")
            print(source_path)
            break

        #issue has occured if cant find the problems associated with *_1 or *_1_1
        while len(current_search_code.split("_")) < 4:

            if os.path.exists(problems_path):
                my_problem = Problems(problems_path)
                break
            else:
                current_search_code += "_1"
                problems_path = "problems/" + current_search_code + ".png"

        if my_problem is None:
            print("Error: failed to find the problems path ->")
            print("note: failed testing not of form *_*_*_1 but *_*_1")
            print(problems_path)
            break

        #output the solutions, determine if they are correct

        my_solutions = Solutions(my_problem, my_source)
        print(my_solutions)

        #update the search code to find the next
        code_items = current_search_code.split("_")
        current_search_code = "" + code_items[0] + "_" + str(int(code_items[1]) + 1)
        

else:
    #just search for the one
    pass



