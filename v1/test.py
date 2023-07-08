# import cv2
# import pytesseract
# from Problems import Problems
# from Source import Source
# from Solutions import Solutions
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# img = cv2.imread('test2.png')

# text = pytesseract.image_to_string(img)
# #print(text)

# my_prob = Problems(text)
# print(my_prob)

# my_source = Source("source1.txt")
# print(my_source)

# my_solutions = Solutions(my_prob, my_source)

# print(my_solutions)

string = "\n   example string with leading and trailing spaces   \n"
cleaned_string = string.strip()
print(cleaned_string)



