import numpy as np 
import fitz
import os 
import re


# # read pdf

# # Get the number of pages that the pdf has (in this case 2)
# doc = fitz.open("Sammelzeugnis.pdf")

# ects_raw = []
# grade_raw = []
# # get the date from all pages
# for i in range(doc.page_count):
#     page = doc.load_page(i) 
#     ects_raw.append(re.findall(r"(\d+.\d+) ECTS", page.get_text()))
#     grade_raw.append(re.findall(r"Note: (\d+)", page.get_text()))

# ects = []
# for i, data in enumerate(ects_raw):
#     for j in data:
#         ects.append(j)


# grades = []
# for i, data in enumerate(grade_raw):
#     for j in data:
#         grades.append(j)

# print(ects)
# print(grades)


# def calculation(ects, grades):
#     ects = np.array(ects, dtype=float)
#     grades = np.array(grades, dtype=float)
#     average_grade = np.sum(ects * grades) / np.sum(ects)
#     return average_grade

class Schnittrechner:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.ects_raw = []
        self.grade_raw = []
        self.ects = []
        self.grades = []
        self.average_grade = 0
        self.doc = fitz.open(self.pdf_path)

    def get_ects(self):
        for i in range(self.doc.page_count):
            page = self.doc.load_page(i) 
            self.ects_raw.append(re.findall(r"(\d+.\d+) ECTS", page.get_text()))
        for i, data in enumerate(self.ects_raw):
            for j in data:
                self.ects.append(j)
        return self.ects
    
    def get_grades(self):
        for i in range(self.doc.page_count):
            page = self.doc.load_page(i) 
            self.grade_raw.append(re.findall(r"Note: (\d+)", page.get_text()))
        for i, data in enumerate(self.grade_raw):
            for j in data:
                self.grades.append(j)
        return self.grades
    
    def calculation_given(self, ects, grades):
        ects = np.array(ects, dtype=float)
        grades = np.array(grades, dtype=float)
        self.average_grade = np.sum(ects * grades) / np.sum(ects)
        return self.average_grade
    
    def calculation(self):
        self.average_grade = np.sum(np.array(self.ects,dtype=float) * np.array(self.grades, dtype=float)) / np.sum(np.array(self.ects, dtype=float))
        return self.average_grade



if __name__ == "__main__":
    input = input("Bitte gib den Namen der PDF Datei ein: ")
    path = os.getcwd()
    pdf_path = os.path.join(path, "Daten", input)
    rechner = Schnittrechner(pdf_path)
    ects = rechner.get_ects()
    # print(np.array(ects, dtype=float))
    grades = rechner.get_grades()
    # print(np.array(grades, dtype=float))
    average_grade = rechner.calculation()
    print(f"Dein Notenschnitt ist: {average_grade}")

# change datatype of ects and grades to float
# ects = np.array(ects, dtype=float)
# grades = np.array(grades, dtype=float)

# print(ects)
# print(grades)


# calculate the average grade (ects * grade) / sum(ects)
# average_grade = np.sum(ects * grades) / np.sum(ects)
# print(average_grade)
# page = doc.load_page(0)
# print(doc.page_count)




# Another way of doing it. 
# arr = []
# for i in ects:
#     arr = arr+i
# print(arr)