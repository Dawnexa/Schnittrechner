import fitz
import os 
import re
from utils import *



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

    Important methods:
        get_ects: Get ECTS from PDF file
        get_grades: Get grades from PDF file
        get_sum_ects: Get sum of ECTS from PDF file
        calculation_given: Calculate average grade with given ECTS and grades
        calculation: Calculate average grade with ECTS and grades from PDF file
    """
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.ects_raw = []
        self.grade_raw = []
        self.ects = []
        self.grades = []
        self.average_grade = 0
        self.doc = fitz.open(self.pdf_path)
        self.pue_etcs = 0 # PUEs counter
        self.vo_ects = 0 # VOs counter
        self.ue_ects = 0 # UEs counter
        self.lp_ects = 0 # Lps counter
        self.vu_ects = 0 # VUs counter
        self.modulprüfung_ects = 0 # Modulprüfungen counter
        self.se_ects = 0

    @property
    def pdf_path(self):
        return self._pdf_path
    
    @pdf_path.setter
    def pdf_path(self, pdf_path):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError("The file does not exist")
        elif not pdf_path.endswith(".pdf"):
            raise TypeError("The file is not a PDF file")
        elif not pdf_path:
            raise ValueError("The path is empty")
        else:
            self._pdf_path = pdf_path

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
        if len(self.ects) == 0:
            return 0
        else:
            self.sum_ects = get_sum(self.ects)
        return self.sum_ects
    
    def calculation_given(self, ects, grades):
        """Calculate average grade with given ECTS and grades

        Args:
            ects (list): ECTS
            grades (list): Grades

        Returns:
            float: Average grade
        """
        if get_sum(ects) == 0:
            return 0
        else:
            self.average_grade = get_multsum(ects, grades) / get_sum(ects)
            return self.average_grade
    
    def calculation(self):
        """Calculate average grade with ECTS and grades from PDF file
        
        Returns:
            float: Average grade"""
        if get_sum(self.ects) == 0:
            return 0
        else:
            self.average_grade = get_multsum(self.ects, self.grades) / get_sum(self.ects)
            return self.average_grade
        
    def get_some_ects(self):
        """Get ECTS from PDF file

        Returns:
            self.vo_ects (float): ECTS for VO
            self.ue_ects (float): ECTS for UE
            self.pue_etcs (float): ECTS for PUE
            self.vu_ects (float): ECTS for VU
            self.lp_ects (float): ECTS for LP
            self.modulprüfung_ects (float): ECTS for Modulprüfung
            self.se_ects (float): ECTS for SE
        """
        for i in range(self.doc.page_count):
            page = self.doc.load_page(i)
            text = page.get_text()
            # print(text)
            
            ects_vo, ects_ue, ects_pue, ects_vu, ects_lp, ects_modulpruefung, ects_se = get_ects_per_stuff(text)
            self.vo_ects += get_sum(ects_vo)
            self.ue_ects += get_sum(ects_ue)
            self.pue_etcs += get_sum(ects_pue)
            self.vu_ects += get_sum(ects_vu)
            self.lp_ects += get_sum(ects_lp)
            self.modulprüfung_ects += get_sum(ects_modulpruefung)
            self.se_ects += get_sum(ects_se)

        return self.vo_ects, self.ue_ects, self.pue_etcs, self.vu_ects, self.lp_ects, self.modulprüfung_ects, self.se_ects
    

    def get_ects_per_semester(self):
        """Get ECTS from PDF file

        Returns:
            ects (list): ECTS
        """
        text_all = ""
        for i in range(self.doc.page_count):
            page = self.doc.load_page(i) 
            text = page.get_text()
            text_all += text

        semester = []
        ects = {}
        semester = get_semesters(text_all, semester)
        ects = extract_ects_per_semester(text_all)
        return ects
    
    def semester_ects(self):
        """Get ECTS from PDF file

        Returns:
            ects (dic): ECTS
        """
        sorted_ects = get_relevant_ects_per_semester(self.doc)
        sum_ects_semester = get_sum_ects2(sorted_ects)

        return sum_ects_semester
    
    def get_semester_ects_per_LV(self):
        """Get ECTS from PDF file

        Returns:
            ects (dic): ECTS
        """
        sorted_ects = get_relevant_ects_per_semester(self.doc)
        ects_per_semester = get_semester_ects(sorted_ects)
        return ects_per_semester



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

    