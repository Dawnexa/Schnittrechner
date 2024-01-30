import numpy as np 
import fitz
import os 
import re



class Schnittrechner:
    """Class to calculate the average grade of a PDF file

    Args:
        pdf_path (str): Path to PDF file
    
    Attributes:
        pdf_path (str): Path to PDF file
        ects_raw (list): List of ECTS from PDF file
        grade_raw (list): List of grades from PDF file
        ects (list): List of ECTS as float
        grades (list): List of grades as float
        average_grade (float): Average grade
        doc (fitz.Document): PDF file
    """
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.ects_raw = []
        self.grade_raw = []
        self.ects = []
        self.grades = []
        self.average_grade = 0
        self.doc = fitz.open(self.pdf_path)

    def get_ects(self):
        """Get ECTS from PDF file
        
        Returns:
            list: ECTS"""
        for i in range(self.doc.page_count):
            page = self.doc.load_page(i) 
            self.ects_raw.append(re.findall(r"(\d+.\d+) ECTS", page.get_text()))
        for i, data in enumerate(self.ects_raw):
            for j in data:
                self.ects.append(j)
        return self.ects
    
    def get_grades(self):
        """Get grades from PDF file

        Returns:
            list: Grades"""
        for i in range(self.doc.page_count):
            page = self.doc.load_page(i) 
            self.grade_raw.append(re.findall(r"Note: (\d+)", page.get_text()))
        for i, data in enumerate(self.grade_raw):
            for j in data:
                self.grades.append(j)
        return self.grades
    def get_sum_ects(self):
        """Get sum of ECTS from PDF file

        Returns:
            float: Sum of ECTS"""
        self.sum_ects = np.sum(np.array(self.ects, dtype=float))
        return self.sum_ects
    
    def calculation_given(self, ects, grades):
        """Calculate average grade with given ECTS and grades

        Args:
            ects (list): ECTS
            grades (list): Grades

        Returns:
            float: Average grade
        """
        ects = np.array(ects, dtype=float)
        grades = np.array(grades, dtype=float)
        self.average_grade = np.sum(ects * grades) / np.sum(ects)
        return self.average_grade
    
    def calculation(self):
        """Calculate average grade with ECTS and grades from PDF file
        
        Returns:
            float: Average grade"""
        self.average_grade = np.sum(np.array(self.ects,dtype=float) * np.array(self.grades, dtype=float)) / np.sum(np.array(self.ects, dtype=float))
        return self.average_grade

    def main(self, filepath):
        path = os.getcwd()
        filepath = filepath + ".pdf"
        pdf_path = os.path.join(path, "Daten", filepath)
        rechner = Schnittrechner(pdf_path)
        ects = rechner.get_ects()
        # print(np.array(ects, dtype=float))
        grades = rechner.get_grades()
        # print(np.array(grades, dtype=float))
        average_grade = rechner.calculation()
        return average_grade
